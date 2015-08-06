# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import colorizer
import HTMLParser

def colorize_file(cp_exp_file):
	output_file = "colored_anki_input.txt"
	h = HTMLParser.HTMLParser()

	with open(cp_exp_file, "r") as f:
		with open(output_file, "w") as out:
			line = f.readline()
			out.write(line)
			for line in f:
				(hanzi, english, pinyin) = line.decode("utf-8").split("\t")
				unic_pinyin = h.unescape(pinyin)
				(color_hanzi, color_pinyin) = colorizer.colorize_chinese(hanzi, unic_pinyin)
				color_line = color_hanzi + "\t" + color_pinyin + "\t" + english + "\n"
				out.write(color_line.encode('utf8'))
