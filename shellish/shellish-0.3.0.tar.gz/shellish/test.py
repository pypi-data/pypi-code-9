import shellish

p = shellish.vt100_print
t = shellish.tabulate

p('asdf')
p('asdf', 'asdfasdf')
p('asdf', 'asdfasdf')
p('<b>bold</b> normal')
p('normal <b>bold</b> normal')

#t([['%d %d' % (i, ii), 'a' * i * ii] for i in range(1, 10) for ii in range(1, 5)])
#t(iter([['%d %d' % (i, ii), 'a' * i * ii] for i in range(1, 10) for ii in range(1, 5)]))
#t(iter([['%d %d' % (i, ii), 'a' * i * ii] for i in range(1, 10) for ii in range(1, 5)]), flex=False)
#t(iter([['%d %d' % (i, ii), 'a' * i * ii] for i in range(1, 10) for ii in range(1, 5)]), width=80)
#t(iter([['%d %d' % (i, ii), 'a' * i * ii] for i in range(1, 10) for ii in range(1, 5)]), header=False)
t(iter([['%d %d' % (i, ii), 'a' * i * ii, 'b' * (i * ii + 10), 'casdfasdfasdf', 'ddddddddddddddd' * ii] for i in range(1, 10) for ii in range(1, 6)]))
