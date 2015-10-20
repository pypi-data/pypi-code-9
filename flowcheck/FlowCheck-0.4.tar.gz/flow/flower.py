
__author__ = 'hellflame'
from os import popen
from re import compile, I
from sys import argv

result = popen("ip -s link").readlines()
net_count = result.__len__() / 6
if net_count == 0:
    print "network card down!!!"
    exit(1)


split = {}
reg_card_head = compile(": (.+?):", I)
reg_card_state = compile("<(.+?)>", I)
head = result[0::6]
for i in head:
    index = head.index(i)
    rx = result[index * 6 + 3].strip(" ").replace("   ", ' ').split(" ")
    tx = result[index * 6 + 5].strip(" ").replace("   ", ' ').split(" ")
    tmp = []
    for r in rx:
        if r.isdigit():
            tmp.append(r)
            break
    for t in tx:
        if t.isdigit():
            tmp.append(t)
            break
    split[reg_card_head.findall(i)[0]] = {"state": reg_card_state.findall(i)[0],
                                          "receive": tmp[0],
                                          "trans": tmp[1]}

for i in split:
    split[i]['total'] = int(split[i]['receive']) + int(split[i]['trans'])


def human_read(data):
    scale = ["B", "KB", "MB", "GB", "TB", "PB"]
    index = 0
    while data > 1024:
        data = data / 1024.0
        index += 1
    return "\033[01;33m{}\033[00m \033[01;31m{}\033[00m".format(float("%0.3f" % data), scale[index])


def total_info():
    total_r = 0
    total_t = 0
    total = 0
    for i in split:
        total_r += int(split[i]['receive'])
        total_t += int(split[i]['trans'])
        total += split[i]['total']
    print "\tTotal Receive {}".format(human_read(total_r))
    print "\tTotal Send {}".format(human_read(total_t))
    print "\n\tTotal Trans Flow {}".format(human_read(total))


def main():
    if len(argv) <= 1:
        total_info()
    else:
        if "-h" in argv or "--help" in argv:
            print """
            --help or -h : show this menu
            --list or -l : show all the network card
            --all or -a : [default choice] show total flow info (all network card in total)
            [ eth ] : specify network card flow info(use --list or -l to check the network card)
            """
        elif "--list" in argv or "-l" in argv:
            for i in split:
                print "\t==> {}".format(i)
        elif "--all" in argv or "-a" in argv:
            total_info()
        else:
            eth = argv[1]
            if eth not in split:
                print "\tyou don't have network card named {} !!".format(eth)
                print "\tuser --list or -l to check out ~~~"
            else:
                print "\tdetails about {} :".format(eth)
                print "\ttotal receive {}".format(human_read(int(split[eth]['receive'])))
                print "\ttotal send {}".format(human_read(int(split[eth]['trans'])))
                print "\n\ttotal trans flow {}".format(human_read(split[eth]['total']))
    exit(0)

if __name__ == '__main__':
    main()


