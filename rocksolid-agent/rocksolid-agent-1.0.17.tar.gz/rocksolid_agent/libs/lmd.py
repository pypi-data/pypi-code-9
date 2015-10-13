class LMD:
    def __init__(self, agent):
        from base import bcolors

        self.bcolors = bcolors
        self.agent   = agent


    def cmd (self, cmd, args):
        # Maldet execution
        # -s, --restore FILE|SCANID
        #    Restore file from quarantine queue to orginal path or restore all items from
        #    a specific SCANID
        #    e.g: maldet --restore /usr/local/maldetect/quarantine/config.php.23754
        #    e.g: maldet --restore 050910-1534.21135
        #
        # -q, --quarantine SCANID
        #    Quarantine all malware from report SCANID
        #    e.g: maldet --quarantine 050910-1534.21135
        #
        # -n, --clean SCANID
        #    Try to clean & restore malware hits from report SCANID
        #    e.g: maldet --clean 050910-1534.21135

        if   cmd == 'restore' and len(args[scanid]) > 0:
            args = lmd_path + " --restore "    + args[scanid]
        elif cmd == 'restore' and len(args[file]) > 0:
            args = lmd_path + " --restore "    + args[file]
        elif cmd == 'quarantine' and len(args[scanid]) > 0:
            args = lmd_path + " --quarantine " + args[scanid]
        elif cmd == 'clean' and len(args[scanid]) > 0:
            args = lmd_path + " --clean "      + args[scanid]

        self.agent.fb(1, 'Executing Maldet integrated command: ' + cmd)
        shell = subprocess.Popen([lmd_path, args], stdout=subprocess.PIPE)
        result, _ = shell.communicate()

        return result


    def scan (self):
        import os
        import re
        import fnmatch

        lmd_path     = '/usr/local/maldetect'
        results      = {}
        file_list     = {}
        nr_found     = 0

        #try:
        if ( os.path.exists(lmd_path)):
            self.agent.fb(1, 'Maldet found... Processing files')

            # Walk the folder
            for root, dirs, files in os.walk(lmd_path + '/sess'):
                for basename in files:
                    filename  = os.path.join(root, basename)

                    if (fnmatch.fnmatch(basename, 'session.[0-9]*')):
                        self.agent.fb(1, 'Found session file, analysing ' + filename)
                        # Read entire file into memory
                        content = open(filename, 'rb').read(512000) # Read maximum of 500KB into memory  << re-open because need larger sample

                        # re.DOTALL = multiline search
                        result             = re.search('SCAN ID: (.*?)\n'      , content, flags=re.DOTALL)
                        if result:
                            scan_id        = result.group(1)
                        else:
                            scan_id        = ''

                        result             = re.search('TIME: (.*?)\n'         , content, flags=re.DOTALL)
                        if result:
                            time           = result.group(1)
                        else:
                            time           = ''

                        result             = re.search('PATH: (.*?)\n'         , content, flags=re.DOTALL)
                        if result:
                            path           = result.group(1)
                        else:
                            path           = ''

                        result             = re.search('RANGE: (.*?)\n'        , content, flags=re.DOTALL)
                        if result:
                            range          = result.group(1)
                        else:
                            range          = ''

                        result             = re.search('TOTAL FILES: (.*?)\n'  , content, flags=re.DOTALL)
                        if result:
                            total_files    = result.group(1)
                        else:
                            total_files    = 0

                        result             = re.search('TOTAL HITS: (.*?)\n'   , content, flags=re.DOTALL)
                        if result:
                            total_hits     = result.group(1)
                        else:
                            total_hits     = 0

                        result             = re.search('TOTAL CLEANED: (.*?)\n', content, flags=re.DOTALL)
                        if result:
                            total_cleaned  = result.group(1)
                        else:
                            total_cleaned  = 0

                        clean_id           = re.split('[.]', scan_id)[1]

                        #self.agent.fb(1, 'scan_id ' + scan_id)
                        #self.agent.fb(1, 'clean_id ' + clean_id)
                        #self.agent.fb(1, 'time ' + time)
                        #self.agent.fb(1, 'path ' + path)
                        #self.agent.fb(1, 'range ' + range)
                        #self.agent.fb(1, 'total_files ' + total_files)
                        #self.agent.fb(1, 'total_hits ' + total_hits)
                        #self.agent.fb(1, 'total_cleaned ' + total_cleaned)

                        if int(total_hits) > 0:
                            # LMD had hits, gather them
                            hits_filename    = lmd_path + '/sess/session.hits.' + scan_id
                            self.agent.fb(1, 'Analysing hits file ' + hits_filename)

                            # Read entire file into memory
                            hits_content    = open(hits_filename, 'rb').read(512000) # Read maximum of 500KB into memory  << re-open because need larger sample
                            lines           = hits_content.split('\n')
                            for line in lines:
                                items = line.split(' : ', 1)
                                nr = int(lines.index(line))
                                self.agent.fb(1, 'NR lines index hits file ' + str(nr))
                                self.agent.fb(1, 'infection: ' + items[0])
                                self.agent.fb(1, 'path: ' + items[1])
                                file_list[nr] = {
                                    'action'    : 'hit',
                                    'infection' : items[0],
                                    'path'      : items[1]
                                }

                        if int(total_cleaned) > 0:
                            # LMD has cleaned files, gather them
                            cleaned_filename = lmd_path + '/sess/clean.' + clean_id
                            self.agent.fb(1, 'Analysing cleaned file ' + cleaned_filename)

                            # Read entire file into memory
                            cleaned_content  = open(cleaned_filename, 'rb').read(512000) # Read maximum of 500KB into memory  << re-open because need larger sample
                            lines            = cleaned_content.split('\n')

                            print cleaned_content

                            for line in lines:
                                items = line.split(' : ', 1)
                                nr = int(lines.index(line))
                                self.agent.fb(1, 'NR lines index cleaned file ' + str(nr))
                                self.agent.fb(1, 'infection: ' + items[0])
                                self.agent.fb(1, 'path: ' + items[1])
                                file_list[nr] = {
                                    'action'    : 'cleaned',
                                    'infection' : items[0],
                                    'path'      : items[1]
                                }


                        results[nr_found] = {
                            'scan_id'       : scan_id,
                            'time'          : time,
                            'path'          : path,
                            'range'         : range,
                            'total_files'   : total_files,
                            'total_hits'    : total_hits,
                            'total_cleaned' : total_cleaned,
                            'files'         : file_list,
                        }
                        nr_found += 1

                    #else:
                        #self.agent.fb(1, 'No match on file ' + basename)

        else:
            self.agent.fb(1, 'Maldet not found... Skipping')
        #except:
        #    pass

        return results