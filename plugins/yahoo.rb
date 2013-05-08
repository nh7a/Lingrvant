# Yahoo!

require 'net/http'

module Lingrvant
  class Yahoo < Plugin
    def help
      "!yf symbol"
    end

    def on_message(text, params)
      case text
        when /^\$(\w+)\s*$/
          cmd_yf([$1])
        else
          super
      end
    end

    def cmd_yf(argv)
      chart = 'http://chart.finance.yahoo.com/z?s=%s&t=1y&q=l&l=on&z=l&p=m50,e200,v&.png' % argv[0]
      q = self.get_quotes(argv[0])
      if q
        "#{chart}\n#{q['name']} (#{q['symbol']})\n#{q['last trade']} #{q['change'][0]} (#{q['change'][1]})\nP/E: #{q['p/e']}"
      else
        chart
      end
    end

    def get_quotes(symbol)
      response = Net::HTTP.get_response('download.finance.yahoo.com', "/d/quotes.csv?f=snl1crx&s=#{symbol}")
      res = response.body.split(',')
      {'symbol' => res[0].gsub(/"/, ''),
       'name' => res[1].gsub(/"/, ''),
       'last trade' => res[2],
       'p/e' => res[4],
       'change' => res[3].gsub(/"/, '').split(' - ')}
    end
  end

  Bot.register(Yahoo)
end
