'''
requests.packages.urllib3.disable_warnings()
if __name__ == '__main__':
    import sys
    import random
    infile = sys.argv[1]
    stime = time.time()
    banlist =  open(infile, 'r').readlines()
    banlist = banlist[:20]
#    banlist = [random.choice(banlist) for x in xrange(200)]
    banlist = [ip.rstrip() for ip in banlist]
    processed = 0
    t = Tapioca()
    ip_info = defaultdict(dict)
    ip_info.update(json.load(open('_'+infile+'.json','r')))

    banlist = [b for b in banlist if b not in ip_info['sgraph']]



    for ips in t.chunker(banlist,10):
#        try:
        p = t.process_ips(ips)
#        except:
#            print 'ERROR! Skipping:  \n' + '  \n'.join(ips)
#            continue
        for table in p:
            ip_info[table].update(p[table])
        with open('_'+infile+'.json','w') as outfile:
            outfile.write(json.dumps(ip_info))
        status = 'Processed {n}/{t} in {s} seconds...'
        print status.format(n=len(ip_info['sgraph'].keys()),
                            t=len(banlist),
                            s=time.time()-stime)
    with open('_'+infile+'.json','w') as outfile:
        outfile.write(json.dumps(ip_info))
    print "Done. Processed {n} items in {t} seconds.".format(
                                n=len(banlist),
                                t=time.time()-stime)
'''
