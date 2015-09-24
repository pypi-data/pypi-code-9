#!/usr/bin/env python3
"""
|0x0001 │  p  │ the read is paired in sequencing                 │
│0x0002 │  P  │ the read is mapped in a proper pair              │
│0x0004 │  u  │ the query sequence itself is unmapped            │
│0x0008 │  U  │ the mate is unmapped                             │
│0x0010 │  r  │ strand of the query (1 for reverse)              │
│0x0020 │  R  │ strand of the mate                               │
│0x0040 │  1  │ the read is the first read in a pair             │
│0x0080 │  2  │ the read is the second read in a pair            │
│0x0100 │  s  │ the alignment is not primary                     │
│0x0200 │  f  │ the read fails platform/vendor quality checks    │
│0x0400 │  d  │ the read is either a PCR or an optical duplicate │
"""
import sys

flag = int(sys.argv[1])

FLAGS = [
	(0x0001, 'p', 'the read is paired in sequencing'),
	(0x0002, 'P', 'the read is mapped in a proper pair'),
	(0x0004, 'u', 'the query sequence itself is unmapped'),
	(0x0008, 'U', 'the mate is unmapped'),
	(0x0010, 'r', 'strand of the query (1 for reverse)'),
	(0x0020, 'R', 'strand of the mate'),
	(0x0040, '1', 'the read is the first read in a pair'),
	(0x0080, '2', 'the read is the second read in a pair'),
	(0x0100, 's', 'the alignment is not primary'),
	(0x0200, 'f', 'the read fails platform/vendor quality checks'),
	(0x0400, 'd', 'the read is either a PCR or an optical duplicate')
]

short = ''
for f, char, description in FLAGS:
	if flag & f != 0:
		short += char
		print(description)

print(short)
