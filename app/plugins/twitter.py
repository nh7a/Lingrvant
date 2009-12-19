# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib
import math
from lingrvant import Plugin
from demjson import decode as decode_json
import logging


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
      response = self.dispatch(text)
    return response

  def cmd_twu(self, twitterid):
    try:
      url = 'http://twitter.com/users/show.json?screen_name=%s' % twitterid[0]
      f = urllib.urlopen(url)
      res = decode_json(f.read())
      logging.debug("twitterscore: %s" % res)
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
    description = self.search('<meta content="([^"]+?)" name="description" />', html)
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
      url = 'http://search.twitter.com/search.json?rpp=3&q=%s' % self.utf8_str(query)
      f = urllib.urlopen(url)
      res = decode_json(f.read())
      response = ''
      for result in res['results']:
        response += '%s %s %s\n' % (result['profile_image_url'], result['from_user'], result['text'])
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
    response = "%s %s" % (image, screen_name)
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


Plugin.register(Twitter())
