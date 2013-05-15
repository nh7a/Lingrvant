# Twitter

require 'twitter'

module Lingrvant
  class Twitter < Plugin

    def help
      <<EOT
!tw[ust] (query...)
u: show user
s: search query
t: show trends
EOT
    end

    def on_message(text, params)
      case text
        when /^@(\w+)\s*$/
          cmd_twu([$1])
        when /^https?:\/\/twitter.com\/(?:#!\/)?[a-zA-Z0-9_]+\/status(?:es)?\/([0-9]+)/
          cmd_tweet([$1])
        else
          super
      end
    end

    def get_signed_url(url, params)
      "#{url}%#{ self.get_signed_body(url, params) }"
    end

    def twitterscore(u)
      followers = u.followers_count > 0 ? u.followers_count : 1
      friends = u.friends_count > 0 ? u.friends_count : 1
      statuses = u.statuses_count > 0 ? u.statuses_count : 1
      score = Math.log((1 + followers / friends ) * statuses)
      score *= score
      sprintf('%.2f', score)
    rescue
      'N/A'
    end

    def cmd_twu(argv)
      u = ::Twitter.user(argv[0])
      if u
        r = []
        r << "#{u.profile_image_url()}?foo.png #{u.screen_name} #{'(Verified Account)' if u.verified}"
        r << "http://twitter.com/#{u.screen_name}"
        r << "Name: #{u.name}"
        r << "Location: #{u.location}" if u.location
        r << "Web: #{u.url}" if u.url
        r << "Bio: #{u.description}" if u.description
        r << "Status: #{u.status.text}" if u.status && u.status.text
        r << "Connection: #{u.friends_count} friends / #{u.followers_count} followers"
        r << "Tweets: #{u.statuses_count}"
        r << "TwitterScore: #{twitterscore(u)}"
        r.join("\n")
      end
    end

    def cmd_tweet(argv)
      t = ::Twitter.status(argv[0])
      if t
        r = []
        r << "#{t.profile_image_url()}?foo.png #{t.user.screen_name}\n"
        r << "#{t.text}\n"
        r << t.created_at.getlocal(t.user.utc_offset)
        if t.source
          r << " via "
          if t.source =~ /.*>(.+)<\/a>/
            r << $1
          else
            r << t.source
          end
        end
        if t.in_reply_to_screen_name
          r << " in reply to #{t.in_reply_to_screen_name}\n"
        end
        t.media.each do |i|
          r << "#{i.media_url}\n"
        end
        r.join('')
      end
    end
  end

  Bot.register(Twitter)
end
