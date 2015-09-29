# Default delimiters
INPUT1 = '''
pid 2
uptime 675
version 1.2.5 END
pid 1
uptime 2
version 3
END
'''

OUTPUT1 = '''{"pid": "2", "uptime": "675", "version": "1.2.5"}
{"pid": "1", "uptime": "2", "version": "3"}
'''

# --field-delim '=', --record-delim '%\n'
INPUT2 = '''
a=1
b=2
c=3
%
d=4
e=5
f=6
%
'''

OUTPUT2 = '''{"a": "1", "b": "2", "c": "3"}
{"d": "4", "e": "5", "f": "6"}
'''

# --field-delim '=', --entry-delim '|' --record-delim '%\n'
INPUT3 = '''
a=1|b=2|c=3%
d=4|e=5|f=6%
'''

OUTPUT3 = '''{"a": "1", "b": "2", "c": "3"}
{"d": "4", "e": "5", "f": "6"}
'''

# --field-delim '=', --entry-delim '|' --record-delim '%'
INPUT4 = '''
a=1|b=2|c=3%d=4|e=5|f=6%
'''

OUTPUT4 = '''{"a": "1", "b": "2", "c": "3"}
{"d": "4", "e": "5", "f": "6"}
'''

