# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib
import math
from lingrvant import Plugin
from demjson import decode as decode_json
import logging
from datetime import datetime
from time import time
from random import getrandbits
from urllib import urlencode, quote as urlquote
from hashlib import sha1
from hmac import new as hmac
import config


def encode(text):
    return urlquote(str(text), '')

class Twitter(Plugin):
  """Twitter Plugin for Lingrvant"""

  def help(self):
    """Show help."""
    return """!tw[ust] (query...)
u: show user
s: search query
t: show trends"""

  def on_message(self, msg):
    """Message handler."""
    text = msg['text']

    if re.match('^@\w+$', text):
      response = self.cmd_twu([text[1:]])
    else:
      match = re.match('^https?://twitter.com/(?:#!\/)?[a-zA-Z0-9_]+/status(?:es)?/([0-9]+)', text)
      if match:
        response = self.cmd_tweet([match.group(1)])
      else:
        response = self.dispatch(text)
    return response

  def cmd_twf(self, twitterid):
    try:
      url = 'http://api.twitter.com/1.1/statuses/friends.json?screen_name=%s' % twitterid[0]
      url = 'http://api.twitter.com/1.1/statuses/friends.json'
      url = self.get_signed_url(url, screen_name=twitterid[0])
      f = urllib.urlopen(url)
      res = decode_json(f.read())
      logging.debug("twu: %s" % res)
      if 'error' in res:
        return res['error']
      for u in res:
        print u['screen_name']

    except Exception, e:
      logging.info(e)

  def cmd_twu(self, twitterid):
    try:
      url = 'http://api.twitter.com/1.1/users/show.json'
      url = self.get_signed_url(url, screen_name=twitterid[0])
      f = urllib.urlopen(url)
      res = decode_json(f.read())
      logging.debug("twu: %s" % res)
      if 'error' in res:
        return res['error']
      else:
        status = ''
        if res['protected']:
          status = "Protected" 
        elif 'status' in res and 'text' in res['status']:
          status = res['status']['text']
        return self.twu_format(res['profile_image_url'], res['screen_name'], res['name'], res['location'], res['url'], res['description'], status, res['friends_count'], res['followers_count'], res['statuses_count'], res['verified'])

    except Exception, e:
      logging.info(e)

    logging.debug('trying without API')
    url = 'http://twitter.com/%s' % twitterid[0]
    f = urllib.urlopen(url)
    html = f.read()
    html = html.replace("\n", '')
    screen_name = self.search('<meta content="([^"]+?)" name="page-user-screen_name" />', html)
    description = self.search('<span class="bio">([^"]+?)</span>', html)
    image = self.search('"profile-image"[^"]+"(http[^"]+?)"', html)
    status = self.search('<ol class="statuses" id="timeline">.*?<span class="entry-content">(.*?)</span>', html)
    friends = self.search('<span id="following_count" class="stats_count numeric">([0-9,\. ]+)</span>', html)
    followers = self.search('<span id="follower_count" class="stats_count numeric">([0-9,\. ]+)</span>', html)
    tweets = self.search('<li id="profile_tab"><a href="/.*" accesskey="u"><span id="update_count" class="stat_count">([0-9,\. ]+)</span><span>Tweets</span></a></li>', html)
    address = self.search(r'<address>(.*)</address>', html)
    name = self.search(r'<li><span class="label">Name</span>(.*?)</li>', address)
    location = self.search(r'<li><span class="label">Location</span>(.*?)</li>', address)
    web = self.search(r'<li><span class="label">Web</span>(.*?)</li>', address)
    verified = False
    return self.twu_format(image, screen_name, name, location, web, description, status, friends, followers, tweets, verified)

  def cmd_tws(self, query):
    if len(query) == 0:
      return
    query = ' '.join(query)
    try:
      url = 'http://search.twitter.com/search.json'
      params = {'rpp': '3', 'q': self.utf8_str(query)}
      params = urllib.urlencode(params)
      f = urllib.urlopen(url, params)
      res = decode_json(f.read())
      logging.info(res)
      response = ''
      for result in res['results']:
        response += '%s?foo.png %s %s\n' % (result['profile_image_url'], result['from_user'], result['text'])
      return response

    except Exception, e:
      logging.info(e)

  def cmd_twt(self, argv):
    try:
      url = 'http://search.twitter.com/trends.json'
      f = urllib.urlopen(url)
      res = decode_json(f.read())
      response = ''
      for trend in res['trends']:
        response += '%s %s\n' % (trend['name'], trend['url'])
      return response

    except Exception, e:
      logging.info(e)

  def cmd_tweet(self, argv):
    tweetid = argv[0]
    try:
      url = 'http://api.twitter.com/1.1/statuses/show/%s.json' % tweetid
      url = 'http://api.twitter.com/1.1/statuses/show.json'
      url = self.get_signed_url(url, id=tweetid, include_entities='true')

      f = urllib.urlopen(url)
      res = decode_json(f.read())
      logging.debug('json: %r', res)
      if 'error' in res:
        return res['error']

      media_urls = []
      text = res['text']
      try:
          for media in res['entities']['media']:
              text = text.replace(media['url'], media['display_url'])
              media_urls.append(media['media_url'])
      except:
          pass
      response = ''
      response = "%s?foo.png %s\n" % (res['user']['profile_image_url'], res['user']['screen_name'])
      response += "%s\n" % text
      response += self.relative_timestamp(res['created_at'])
      if res['source']:
        match = re.match('.*>(.+)</a>', res['source'])
        if match:
          source = match.group(1)
        else:
          source = res['source']
        response += " via %s" % source
      if res['in_reply_to_screen_name']:
        response += " in reply to %s" % res['in_reply_to_screen_name']
      if len(media_urls):
          response += "\n%s" % "\n".join(media_urls)
      return response

    except Exception, e:
      logging.info(e)
      return e

  def search(self, regex, text):
    result = re.search(regex, text)
    if result:
      return result.group(1)

  def twitterscore(self, friends, followers, statuses):
    logging.debug("twitterscore: %s %s %s" % (friends, followers, statuses))
    score = 'N/A'
    try:
      n1 = int(friends.replace(',','').replace('.',''))
      n2 = int(followers.replace(',','').replace('.',''))
      n3 = int(statuses.replace(',','').replace('.',''))
    except:
      n1 = int(friends)
      n2 = int(followers)
      n3 = int(statuses)
    try:
      score = math.log((1 + n2 / n1) * n3)
      score *= score
      score = '%.2f' % score
    except:
      pass
    return score

  def twu_format(self, image, screen_name, name, location, web, description, status, friends, followers, tweets, verified):
    score = self.twitterscore(friends, followers, tweets)
    response = "%s?foo.png %s" % (image, screen_name)
    if verified:
      response += " (Verified Account)"
    response += "\n"
    response += "http://twitter.com/%s\n" % screen_name
    response += "Name: %s\n" % name
    if location and len(location):
      response += "Location: %s\n" % location
    if web and len(web):
      response += "Web: %s\n" % web
    if description and len(description):
      response += "Bio: %s\n" % description
    if status and len(status):
      response += "Status: %s\n" % status
    response += "Connection: %s friends / %s followers\n" % (friends, followers)
    response += "Tweets: %s\n" % tweets
    response += "TwitterScore: %s" % score

    re_tag = re.compile('<[a-zA-Z\/][^>]*?>')
    return re_tag.sub('', response).strip()


  def relative_timestamp(self, timestamp):
    created_at = datetime.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y")
    delta = datetime.utcnow() - created_at

    if delta.days == 0:
      d = delta.seconds
      if d == 1:
        return "a second ago"
      if d < 60:
        return "%d seconds ago" % d
  
      d /= 60
      if d == 1:
        return "about a minute ago"
      if d < 60:
        return "%d minutes ago" % d

      d /= 60
      if d == 1:
        return "about an hour ago"
      if d < 24:
        return "%d hours ago" % d
    else:  
      d = delta.days
      if d == 1:
        return "Yesterday"
      if d < 7:
        return "%d days ago" % d

    return "%s" % created_at

  def get_signed_url(self, __url, **extra_params):
    return '%s?%s'%(__url, self.get_signed_body(__url, **extra_params))

  def get_signed_body(self, __url,**extra_params):
    kwargs = {
      'oauth_consumer_key': config.twitter_consumer_key,
      'oauth_signature_method': 'HMAC-SHA1',
      'oauth_version': '1.0',
      'oauth_timestamp': int(time()),
      'oauth_nonce': getrandbits(64),
      'oauth_token': config.twitter_oauth_token,
      }

    kwargs.update(extra_params)
    key = encode(config.twitter_consumer_secret) + '&' + encode(config.twitter_oauth_token_secret)
    message = '&'.join(map(encode, [
          'GET', __url, '&'.join(
            '%s=%s' % (encode(k), encode(kwargs[k])) for k in sorted(kwargs)
            )
          ]))

    kwargs['oauth_signature'] = hmac(
      key, message, sha1
      ).digest().encode('base64')[:-1]

    return urlencode(kwargs)


Plugin.register(Twitter())
