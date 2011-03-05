# coding: utf-8
# Copyright (c) 2011 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

from lingrvant import Plugin
import logging


HIRAGANYDIC = {"a":"あ","i":"い","u":"う","e":"え","o":"お","A":"ア","I":"イ","U":"ウ","E":"エ","O":"オ","ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ","KA":"カ","KI":"キ","KU":"ク","KE":"ケ","KO":"コ","kya":"きゃ","kyi":"きぃ","kyu":"きゅ","kye":"きぇ","kyo":"きょ","KYA":"キャ","KYI":"キィ","KYU":"キュ","KYE":"キェ","KYO":"キョ","ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご","GA":"ガ","GI":"ギ","GU":"グ","GE":"ゲ","GO":"ゴ","gya":"ぎゃ","gyi":"ぎぃ","gyu":"ぎゅ","gye":"ぎぇ","gyo":"ぎょ","GYA":"ギャ","GYI":"ギィ","GYU":"ギュ","GYE":"ギェ","GYO":"ギョ","sa":"さ","si":"し","su":"す","se":"せ","so":"そ","SA":"サ","SI":"シ","SU":"ス","SE":"セ","SO":"ソ","za":"ざ","zi":"じ","zu":"ず","ze":"ぜ","zo":"ぞ","ZA":"ザ","ZI":"ジ","ZU":"ズ","ZE":"ゼ","ZO":"ゾ","sya":"しゃ","syi":"しぃ","syu":"しゅ","sye":"しぇ","syo":"しょ","SYA":"シャ","SYI":"シィ","SYU":"シュ","SYE":"シェ","SYO":"ショ","sha":"しゃ","shi":"し","shu":"しゅ","she":"しぇ","sho":"しょ","SHA":"シャ","SHI":"シ","SHU":"シュ","SHE":"シェ","SHO":"ショ","zya":"じゃ","zyi":"じ","zyu":"じゅ","zye":"じぇ","zyo":"じょ","ZYA":"ジャ","ZYI":"ジィ","ZYU":"ジュ","ZYE":"ジェ","ZYO":"ジョ","ja":"じゃ","ji":"じ","ju":"じゅ","je":"じぇ","jo":"じょ","JA":"ジャ","JI":"ジ","JU":"ジュ","JE":"ジェ","JO":"ジョ","jya":"じゃ","jyi":"じぃ","jyu":"じゅ","jye":"じぇ","jyo":"じょ","JYA":"ジャ","JYI":"ジィ","JYU":"ジュ","JYE":"ジェ","JYO":"ジョ","ta":"た","ti":"ち","tu":"つ","te":"て","to":"と","TA":"タ","TI":"チ","TU":"ツ","TE":"テ","TO":"ト","da":"だ","di":"ぢ","du":"づ","de":"で","do":"ど","DA":"ダ","DI":"ヂ","DU":"ヅ","DE":"デ","DO":"ド","tha":"た゜","thi":"ち゜","thu":"つ゜","the":"て゜","tho":"と゜","THA":"タ゜","THI":"チ゜","THU":"ツ゜","THE":"テ゜","THO":"ト゜","tya":"ちゃ","tyi":"ちぃ","tyu":"ちゅ","tye":"ちぇ","tyo":"ちょ","TYA":"チャ","TYI":"チィ","TYU":"チュ","TYE":"チェ","TYO":"チョ","cya":"ちゃ","cyi":"ちぃ","cyu":"ちゅ","cye":"ちぇ","cyo":"ちょ","CYA":"チャ","CYI":"チィ","CYU":"チュ","CYE":"チェ","CYO":"チョ","na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の","NA":"ナ","NI":"ニ","NU":"ヌ","NE":"ネ","NO":"ノ","nya":"にゃ","nyi":"にぃ","nyu":"にゅ","nye":"にぇ","nyo":"にょ","NYA":"ニャ","NYI":"ニィ","NYU":"ニュ","NYE":"ニェ","NYO":"ニョ","ha":"は","hi":"ひ","hu":"ふ","he":"へ","ho":"ほ","HA":"ハ","HI":"ヒ","HU":"フ","HE":"ヘ","HO":"ホ","ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ","BA":"バ","BI":"ビ","BU":"ブ","BE":"ベ","BO":"ボ","va":"う゛ぁ","vi":"う゛ぃ","vu":"う゛ぅ","ve":"う゛ぇ","vo":"う゛ぉ","VA":"ヴァ","VI":"ヴィ","VU":"ヴ","VE":"ヴェ","VO":"ヴォ","pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ","PA":"パ","PI":"ピ","PU":"プ","PE":"ペ","PO":"ポ","fa":"ふぁ","fi":"ふぃ","fu":"ふ","fe":"ふぇ","fo":"ふぉ","FA":"ファ","FI":"フィ","FU":"フ","FE":"フェ","FO":"フォ","hya":"ひゃ","hyi":"ひぃ","hyu":"ひゅ","hye":"ひぇ","hyo":"ひょ","HYA":"ヒャ","HYI":"ヒィ","HYU":"ヒュ","HYE":"ヒェ","HYO":"ヒョ","fya":"ひゃ","fyi":"ひぃ","fyu":"ひゅ","fye":"ひぇ","fyo":"ひょ","FYA":"ヒャ","FYI":"ヒィ","FYU":"ヒュ","FYE":"ヒェ","FYO":"ヒョ","bya":"びゃ","byi":"びぃ","byu":"びゅ","bye":"びぇ","byo":"びょ","BYA":"ビャ","BYI":"ビィ","BYU":"ビュ","BYE":"ビェ","BYO":"ビョ","pya":"ぴゃ","pyi":"ぴぃ","pyu":"ぴゅ","pye":"ぴぇ","pyo":"ぴょ","PYA":"ピャ","PYI":"ピィ","PYU":"ピュ","PYE":"ピェ","PYO":"ピョ","ma":"ま","mi":"み","mu":"む","me":"め","mo":"も","MA":"マ","MI":"ミ","MU":"ム","ME":"メ","MO":"モ","mya":"みゃ","myi":"みぃ","myu":"みゅ","mye":"みぇ","myo":"みょ","MYA":"ミャ","MYI":"ミィ","MYU":"ミュ","MYE":"ミェ","MYO":"ミョ","ya":"や","yi":"い","yu":"ゆ","ye":"え","yo":"よ","YA":"ヤ","YI":"イ","YU":"ユ","YE":"エ","YO":"ヨ","ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ","RA":"ラ","RI":"リ","RU":"ル","RE":"レ","RO":"ロ","rya":"りゃ","ryi":"りぃ","ryu":"りゅ","rye":"りぇ","ryo":"りょ","RYA":"リャ","RYI":"リィ","RYU":"リュ","RYE":"リェ","RYO":"リョ","wa":"わ","wi":"ゐ","wu":"う","we":"ゑ","wo":"を","WA":"ワ","WI":"ヰ","WU":"ウ","WE":"ヱ","WO":"ヲ","wya":"ゐゃ","wyi":"ゐぃ","wyu":"ゐゅ","wye":"ゐぇ","wyo":"ゐょ","WYA":"ヰァ","WYI":"ヰィ","WYU":"ヰゥ","WYE":"ヰェ","WYO":"ヰォ","nn":"ん","NN":"ン","la":"ぁ","li":"ぃ","lu":"ぅ","le":"ぇ","lo":"ぉ","LA":"ァ","LI":"ィ","LU":"ゥ","LE":"ェ","LO":"ォ","ltu":"っ","LTU":"ッ","lya":"ゃ","lyu":"ゅ","lyo":"ょ","LYA":"ャ","LYU":"ュ","LYO":"ョ","lwa":"ゎ","LWA":"ヮ","xa":"ぁ","xi":"ぃ","xu":"ぅ","xe":"ぇ","xo":"ぉ","XA":"ァ","XI":"ィ","XU":"ゥ","XE":"ェ","XO":"ォ","xtu":"っ","XTU":"ッ","xya":"ゃ","xyu":"ゅ","xyo":"ょ","XYA":"ャ","XYU":"ュ","XYO":"ョ","xwa":"ゎ","XWA":"ヮ",",":"、",".":"。","-":"ー","=":"＝","_":"＿","+":"＋","h,":",","h.":".","`":"‘","1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","7":"7","8":"8","9":"9","0":"0","~":"〜","!":"！","@":"＠","#":"＃","$":"＄","%":"％","^":"＾","&":"＆","*":"＊","(":"（",")":"）","[":"「","]":"」","\\":"￥",";":"；","'":"′","/":"・","{":"『","}":"』","|":"｜",":":"：",'"':"″","<":"＜",">":"＞","?":"？","bb":"っ","cc":"っ","dd":"っ","ff":"っ","gg":"っ","hh":"っ","jj":"っ","kk":"っ","ll":"っ","mm":"っ","pp":"っ","qq":"っ","rr":"っ","ss":"っ","tt":"っ","vv":"っ","ww":"っ","xx":"っ","yy":"っ","zz":"っ","BB":"ッ","CC":"ッ","DD":"ッ","FF":"ッ","GG":"ッ","HH":"ッ","JJ":"ッ","KK":"ッ","LL":"ッ","MM":"ッ","PP":"ッ","QQ":"ッ","RR":"ッ","SS":"ッ","TT":"ッ","VV":"ッ","WW":"ッ","XX":"ッ","YY":"ッ","ZZ":"ッ","n":"ん","N":"ン","n'":"ん","N'":"ン"}

class Hiragany(Plugin):
    """Make Romanized Japanese Hiraganized"""

    def help(self):
        """Help"""
        return """!h [on|off]"""

    def on_message(self, msg):
        """Message handler."""
        key = '%s %s' % (msg['speaker_id'], msg['room'])
        if msg['text'] == '!h on':
            self.memcache.set(key, True, namespace='Hiragany')
            return 'わわわ'

        if self.memcache.get(key, namespace='Hiragany'):
            if msg['text'] == '!h off':
                self.memcache.delete(key, namespace='Hiragany')
                return 'ゎ'
            elif msg['text'][0] != '!':
                return self.convert(msg['text'])

    def normalize(self, src):
        arr = []
        for word in src.split(' '):
            if word != word.upper():
                word = word.lower()
            arr.append(word)
        return ' '.join(arr)

    def convert(self, src):
        src = self.normalize(src)
        arr = []
        skip = 0
        for pos in xrange(len(src)):
            if skip > 0:
                skip -= 1
                continue
            slen = 5
            f = False
            while slen:
                slen -= 1
                temp = src[pos:pos+slen]
                logging.info('slen(%d) temp(%s)', slen, temp)
                if not temp in HIRAGANYDIC: continue
                f = True
                kana = HIRAGANYDIC[temp]
                logging.info('slen(%d) kana(%s)', slen, kana)
                skip = 1 if slen == 2 else slen-1
                if slen == 2:
                    if kana == HIRAGANYDIC['tt'] or kana == HIRAGANYDIC['TT']:
                        skip = 0
                arr.append(str(kana))
                break

            if not f:
                logging.info('pos(%d) src[pos](%s)', pos, src[pos])
                arr.append(str(src[pos]))

        return ''.join(arr)


Plugin.register(Hiragany())
