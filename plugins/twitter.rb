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
      if text =~ /^@\w+/
         cmd_twu([text[1..-1]])
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
        r << "Status: #{u.status.text}" if u.status.text
        r << "Connection: #{u.friends_count} friends / #{u.followers_count} followers"
        r << "Tweets: #{u.statuses_count}"
        r << "TwitterScore: #{twitterscore(u)}"
        r.join("\n")
      end
    end
  end

  Bot.register(Twitter)
end
