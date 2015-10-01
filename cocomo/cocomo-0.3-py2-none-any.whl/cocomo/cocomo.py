"""
Copyright 2015 Chintalagiri Shashank
See the LICENSE file for further information.

Essentially implementing the details written out by David A. Wheeler
and relying on the SLOCCount binary to do all the heavy lifting.
http://www.dwheeler.com/sloccount/sloccount.html
"""

import subprocess
import logging
import yaml
import os
import sys


def main():
    logging.basicConfig(level=logging.INFO)
    projectfolder = sys.argv[1]
    with open(os.path.join(projectfolder, 'cocomo.yaml'), 'r') as f:
        data = yaml.load(f)
        logging.info("Got COCOMO parameters")

    if 'folders' in data.keys():
        folders = [os.path.join(projectfolder, x) for x in data['folders']]
    else:
        folders = [projectfolder]

    addlangs = None
    if 'addlang' in data.keys():
        addlangs = data['addlang']

    headers = ('Very Low', 'Low', 'Nominal', 'High', 'Very High', 'Extra High')

    corrective_factors = {'RELY': (0.75, 0.88, 1.0, 1.15, 1.40, None),
                          'DATA': (None, 0.94, 1.0, 1.08, 1.16, None),
                          'CPLX': (0.70, 0.85, 1.0, 1.15, 1.30, 1.65),
                          'TIME': (None, None, 1.0, 1.11, 1.30, 1.66),
                          'STOR': (None, None, 1.0, 1.06, 1.21, 1.56),
                          'VIRT': (None, 0.87, 1.0, 1.15, 1.30, None),
                          'TURN': (None, 0.87, 1.0, 1.07, 1.15, None),
                          'ACAP': (1.46, 1.19, 1.0, 0.86, 0.71, None),
                          'AEXP': (1.29, 1.13, 1.0, 0.91, 0.82, None),
                          'PCAP': (1.42, 1.17, 1.0, 0.86, 0.70, None),
                          'VEXP': (1.21, 1.10, 1.0, 0.90, None, None),
                          'LEXP': (1.14, 1.07, 1.0, 0.95, None, None),
                          'MODP': (1.24, 1.10, 1.0, 0.91, 0.82, None),
                          'TOOL': (1.24, 1.10, 1.0, 0.91, 0.83, None),
                          'SCED': (1.23, 1.08, 1.0, 1.04, 1.10, None)}

    effort = 2.4
    effort_exponent = 1.05
    schedule = 2.5
    schedule_exponent = 0.38

    if 'type' in data.keys():

        if data['type'] == 'basic':
            logging.info("Basic Mode")
            if 'mode' in data.keys():
                if data['mode'] == 'ORGANIC':
                    effort = 2.4
                    effort_exponent = 1.05
                    schedule = 2.5
                    schedule_exponent = 0.38
                elif data['mode'] == 'SEMIDETACHED':
                    effort = 3.0
                    effort_exponent = 1.12
                    schedule = 2.5
                    schedule_exponent = 0.35
                elif data['mode'] == 'EMBEDDED':
                    effort = 3.6
                    effort_exponent = 1.2
                    schedule = 2.5
                    schedule_exponent = 0.32
        if data['type'] == 'intermediate':
            logging.info("Intermediate Mode")
            if 'mode' in data.keys():
                if data['mode'] == 'ORGANIC':
                    effort = 2.3
                    effort_exponent = 1.05
                    schedule = 2.5
                    schedule_exponent = 0.38
                elif data['mode'] == 'SEMIDETACHED':
                    effort = 3.0
                    effort_exponent = 1.12
                    schedule = 2.5
                    schedule_exponent = 0.35
                elif data['mode'] == 'EMBEDDED':
                    effort = 2.8
                    effort_exponent = 1.2
                    schedule = 2.5
                    schedule_exponent = 0.32

            for k in corrective_factors.keys():
                if k in data.keys():
                    idx = headers.index(data[k])
                    if corrective_factors[k][idx] is not None:
                        factor = corrective_factors[k][idx]
                    else:
                        state = 'before'
                        for idxi, header in enumerate(headers):
                            if idxi == idx:
                                state = 'after'
                            elif corrective_factors[k][idxi] is not None and state == 'after':
                                factor = corrective_factors[k][idxi]
                                break
                            elif corrective_factors[k][idxi] is not None and state == 'before':

                                factor = corrective_factors[k][idxi]
                    logging.info("Applying Corrective Factor : " + k + "=" + str(factor))
                    effort *= factor

    logging.info("Effort : " + str(effort) + " " + str(effort_exponent))
    logging.info("Schedule : " + str(schedule) + " " + str(schedule_exponent))

    command = ['sloccount',
               '--effort', str(effort), str(effort_exponent),
               '--schedule', str(schedule), str(schedule_exponent),
               '--']
    command += folders
    if addlangs:
        for lang in addlangs:
            command += ['--addlang', lang]
    logging.info('Running command : ')
    logging.info(' '.join(command))
    subprocess.call(command)


if __name__ == '__main__':
    main()
