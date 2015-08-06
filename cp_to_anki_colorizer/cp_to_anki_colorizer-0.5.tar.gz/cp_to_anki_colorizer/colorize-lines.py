# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import colorizer
import HTMLParser

hanzi_str = "小林，这是你的桌子。"
pinyin_str = "Xiǎo Lín zhè shì nǐ de zhuōzi"
res = colorizer.colorize_chinese(hanzi_str, pinyin_str)
print res[0]
print res[1]

cp_exp_file = "chinesepod_vocab_anki.txt"
output_file = "chinesepod_vocab_anki_colored.txt"

h = HTMLParser.HTMLParser()

with open(cp_exp_file, "r") as f:
	with open(output_file, "w") as out:
		line = f.readline()
		out.write(line)
		for line in f:
			(hanzi, english, pinyin) = line.decode("utf-8").split("\t")
			unic_pinyin = h.unescape(pinyin)
			(color_hanzi, color_pinyin) = colorizer.colorize_chinese(hanzi, unic_pinyin)
			print color_hanzi, english, color_pinyin
			color_line = color_hanzi + "\t" + color_pinyin + "\t" + english + "\n"
			out.write(color_line.encode('utf8'))
