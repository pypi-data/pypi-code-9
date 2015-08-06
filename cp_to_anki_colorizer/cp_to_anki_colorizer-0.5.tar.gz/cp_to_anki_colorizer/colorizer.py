# -*- coding: utf-8 -*-

#TODO: read in file of tab-delimited stuff to be imported, replace each line with the hanzi and pinyin colorized
    #probably easiest just to build a new file for this, but can do it in place if you want

from __future__ import unicode_literals
import zhon.hanzi, zhon.pinyin, zhon.cedict, zhon.zhuyin
import re


tone_regexes = ["āēīōūǖ", "áéíóúǘ", "ǎěǐǒǔǚ", "àèìòùǜ"]
tone_colors = ["#ac1010", "#f47501", "#326d09", "#183a91"]

def unic_arr_to_str(hanzi_arr):
	return '[' + ', '.join(hanzi_arr) + ']'

def pinyin_tone(pinyin_syllable):
	for i in xrange(len(tone_regexes)):
		if re.search('['+tone_regexes[i]+']', pinyin_syllable):
			return i + 1
	return 0
		
def add_color_html(string, tone):
	if tone == 0:
		return string
	return '<font color="' + tone_colors[tone - 1] + '">' + string + '</font>'
	

def colorize_chinese(hanzi_str, pinyin_str):
	hanzi_arr = re.findall('[%s]' % zhon.hanzi.characters, hanzi_str)
	pinyin_arr = re.findall(zhon.pinyin.syllable, pinyin_str, re.I)
	tones = [pinyin_tone(pinyin_syllable) for pinyin_syllable in re.findall(zhon.pinyin.syllable, pinyin_str, re.I)]

	curr = 0
	colored_hanzi = ""
	colored_pinyin = ""
	for i in xrange(len(hanzi_str)):
		if curr >= len(hanzi_arr) or hanzi_arr[curr] != hanzi_str[i]:
			colored_hanzi += hanzi_str[i]
			continue	

		colored_hanzi += add_color_html(hanzi_arr[curr], tones[curr])
		colored_pinyin += add_color_html(pinyin_arr[curr], tones[curr])
		curr += 1
		
	return (colored_hanzi, colored_pinyin)


hanzi_str = "小林，这是你的桌子。"
pinyin_str = "Xiǎo Lín zhè shì nǐ de zhuōzi" 
res = colorize_chinese(hanzi_str, pinyin_str)
print res[0]
print res[1]

			







