# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from getpass import getuser
from datetime import date, timedelta
from tempfile import TemporaryDirectory, NamedTemporaryFile
from shutil import unpack_archive, copyfile
from os import listdir, walk, makedirs
from os.path import join, split, getsize
from urllib.parse import urlparse
import logging
import hcpsdk
import hcplogs

# instance state identifiers
S_CREATED = 'created'  # instance created
S_READY = 'ready'  # ready for preparing (i.e., canceled)
S_PREPARING = 'preparing'  # preparation has been requested successfully
S_ERROR = 'error'  # an error occured during preparation
S_PREPARED = 'prepared'  # preparation has finished, ready for download
S_DOWNLOAD = 'download'  # download is active


class Handler(object):
    """
    A class that handles the log dowbload for a single HCP target
    """

    def __init__(self, tgt, conf):
        """
        initialize communication to an HCP system

        :param tgt:     a dict holding the params needed to connect
        """
        self.logger = logging.getLogger(__name__ + '.Handler')
        # if type(tgt) != dict:
        #     raise hcplogs.HcplogError('Coding error: type(tgt) == {}, not {}'
        #                            .format(type(tgt), type(dict())))
        self.conf = conf
        self.tgtstr = tgt
        self.tgt = self.conf.targets[tgt]
        self.state = S_CREATED
        self.tmpdir = TemporaryDirectory(
            dir=self.conf.c.get('temporary store',
                                'tempdir',
                                fallback='.'))
        self.logger.debug('Handler initializing for {}'
                          .format(self.tgtstr))

        # Open the session with HCP and mark its log accordingly
        try:
            auth = hcpsdk.NativeAuthorization(self.tgt['user'],
                                              self.tgt['password'])
            self.t = hcpsdk.Target(self.tgt['fqdn'], auth,
                                   port=hcpsdk.P_MAPI)
            self.l = hcpsdk.mapi.Logs(self.t)
            self.l.mark('HCPLOGS begins a log download session '
                        '(remote user={})'.format(getuser()))
        except Exception as e:
            raise hcplogs.HcplogError('Connection to {} failed\n\thint: {}'
                                   .format(self.tgt['fqdn'], e))

    def cancel(self):
        """
        Cancel log preparation

        :raises:    *HcplogsError*
        """
        self.logger.debug('proactively canceling the logdl for {}'
                          .format(self.tgtstr))
        try:
            self.l.cancel()
            self.state = S_READY
        except Exception as e:
            self.state = S_CREATED
            raise hcplogs.HcplogError('cancel log preparation for {} failed\n'
                                   '\thint: {}'.format(self.tgt['fqdn'], e))

    def prepare(self):
        """
        Command HCP to prepare logs for download

        :raises:    *HcplogsError*
        """
        self.logger.debug('starting log preparation for {}'
                          .format(self.tgtstr))

        # ToDo: create start/enddate from what we know
        if self.tgt['last collected']:
            try:
                d = self.tgt['last collected'].split('-')
                startdate = date(int(d[0]), int(d[1]), int(d[2]))
            except Exception as e:
                raise hcplogs.HcplogError('config parameter "last collected" '
                                       'for {} is invalid\n\thint: {}'
                                       .format(self.tgt['fqdn'], e))
        else:
            startdate = date.today() - timedelta(days=31)
        enddate = date.today()

        try:
            self.l.prepare(startdate=startdate, enddate=enddate)
            self.state = S_PREPARING
        except Exception as e:
            self.state = S_CREATED
            raise hcplogs.HcplogError('start log preparation for {} failed\n'
                                   '\thint: {}'.format(self.tgt['fqdn'], e))

        self.tgt['last collected'] = enddate.isoformat()

    def status(self):
        """
        Query HCP for the status of log preparation

        :returns:   True if finished, else False
        """
        self.logger.debug('status query for {}'
                          .format(self.tgtstr))
        try:
            stat = self.l.status()
        except Exception as e:
            raise hcplogs.HcplogError('status query for {} failed\n'
                                   '\thint: {}'.format(self.tgt['fqdn'], e))
        self.logger.debug('status = {}'.format(stat))

        if stat['error']:
            self.state = S_ERROR
        elif stat['readyForStreaming']:
            self.state = S_PREPARED
            return True
        elif stat['streamingInProgress']:
            self.state = S_DOWNLOAD
        elif stat['started']:
            self.state = S_PREPARING

        return False

    def download(self):
        """
        Download the logs from HCP

        :return:    False if not ready for download, else True
        """
        if self.state != S_PREPARED:
            return False

        self.logger.debug('downloading for {}'
                          .format(self.tgtstr))

        try:
            dlhdl = NamedTemporaryFile('w+b', dir=self.tmpdir.name,
                                       delete=False)
        except Exception as e:
            raise hcplogs.HcplogError('creating tempfile for {} failed\n'
                                   '\thint: {}'.format(self.tgt['fqdn'], e))
        self.logger.debug('download will be stored to "{}"'
                          .format(dlhdl.name))

        try:
            self.l.download(hdl=dlhdl, logs=['ACCESS'], progresshook=None)
        except Exception as e:
            raise hcplogs.HcplogError('download for {} failed\n'
                                   '\thint: {}'.format(self.tgt['fqdn'], e))
        else:
            arch = dlhdl.name
            dlhdl.close()
            try:
                self.unpack(arch)
            except Exception as e:
                raise hcplogs.HcplogError('unpacking downloaded file for {} '
                                       'failed\n\thint: {}'
                                       .format(self.tgt['fqdn'], e))
            else:
                return True

    def unpack(self, arch):
        """
        Unzip the logs and copy the required files into the target folder
        structure

        :param arch:    the file containing the downloaded file
        :return:        a list of path/files to transfer
        """
        self.logger.info('unpacking downloaded logs for {}'
                         .format(self.tgtstr))

        # Step 1: unpack the downloaded file
        #         result will be something like this:
        #           HCPLogs-hcp-domain.com-YYYMMDD-HHMM
        #               176.tar.bz2
        #               177.tar.bz2
        #               178.tar.bz2
        #               179.tar.bz2
        #               manifest.csv
        unpack_archive(arch, self.tmpdir.name, format='zip')

        # find the folder where the file was uncompressed to
        archdir = None
        for f in listdir(self.tmpdir.name):
            if f.startswith('HCPLogs-'):
                archdir = f
        self.logger.debug('unpacked into "{}"'.format(join(self.tmpdir.name,
                                                           archdir)))

        # parse the manifest.csv to find out about the individual node's
        # logs
        nodes = self.parsemanifest(join(self.tmpdir.name, archdir,
                                        'manifest.csv'))
        for i in nodes:
            self.logger.debug('parser result: {}'.format(i))
            unpack_archive(join(self.tmpdir.name, i[1]),
                           join(self.tmpdir.name, archdir),
                           format='bztar')
            # now, we have a structure like this:
            #           HCPLogs-hcp-domain.com-YYYMMDD-HHMM
            #               176                       (where 176 is the node id)
            #                   var
            #                       ris
            #                           retired
            #                               access-logs-20151004-0345.tar.bz2
            for j in listdir(join(self.tmpdir.name, i[2], 'var', 'ris',
                                  'retired')):
                unpack_archive(join(self.tmpdir.name, i[2], 'var', 'ris',
                                    'retired', j),
                               join(self.tmpdir.name, i[2], '_logs'),
                               format='bztar')
            # which now ends up here after the prior step:
            #           HCPLogs-hcp-domain.com-YYYMMDD-HHMM
            #               176                       (where 176 is the node id)
            #                   _logs
            #                       20151004-1203
            #                           admin_request.log.0
            #                           http_gateway_request.log.0
            #                           mapi_gateway_request.log.0

            # Now we'll create a list of 2-tuples (files to be transfered,
            #                                      target path/name)
            #   [('./tmpsfr08eb8/HCPLogs-hcp.domain.com-acc-20151005-1152/177/_logs/20151004-2018/admin_request.log.0',
            #     '<node IP>/<year>/admin_request/20151005-1312.log.0'),
            #    ('./tmpsfr08eb8/HCPLogs-hcp.domain.com-acc-20151005-1152/177/_logs/20151004-2018/http_gateway_request.log.0',
            #     '<node IP>/<year>/http_gateway_request/20151005-1312.log.0'),
            #    ('./tmpsfr08eb8/HCPLogs-hcp.domain.com-acc-20151005-1152/177/_logs/20151004-2018/mapi_gateway_request.log.0',
            #     '<node IP>/<year>/mapi_gateway_request/20151005-1312.log.0'),
            #    <etc> ]

            # this is to filter out unwanted logs
            reqlogs = []
            if self.conf.c.getboolean('access logs', 'access',
                                      fallback=False):
                reqlogs.append('http')
            if self.conf.c.getboolean('access logs', 'admin',
                                      fallback=False):
                reqlogs.append('admi')
            if self.conf.c.getboolean('access logs', 'mapi',
                                      fallback=False):
                reqlogs.append('mapi')

            flist = []
            for root, dirs, files in walk(
                    join(self.tmpdir.name, i[2], '_logs')):
                for f in files:
                    if f[:4] not in reqlogs:
                        continue

                    if self.conf.c.getboolean('access logs', 'omit empty',
                                              fallback=True) \
                            and not getsize(join(root, f)):
                        self.logger.debug(
                            'empty file: {}'.format(join(root, f)))
                        continue
                    # path/filename conversion:
                    # from root: ./tmpsfr08eb8/HCPLogs-hcp.domain.com-acc-20151005-1152/177/_logs/20151004-2018
                    #                                                                             ^-split(root)[1]
                    # and file:  http_gateway_request.log.0
                    #            ^-f.split('-')[0]        ^-f.split('-')[2]
                    #
                    # to:   192.168.0.177/2015/mapi_gateway_request/20151005-1312.log.0
                    #       |             |    ^-np[0]              ^-ts          |   ^-np[2]
                    #       +-i[0]        +-ts[:4]                                +-np[1]
                    ts = split(root)[1]
                    np = f.split('.')
                    nn = '.'.join([ts, np[1], np[2]])
                    tf = join(i[0], ts[:4], np[0], nn)
                    flist.append((join(root, f), tf))

            # Now transfer the acquired logfiles to the archive store(s)
            if self.conf.c.getboolean('local archive store', 'enable',
                                      fallback=False):
                self._transferlocal(i[0], flist)
            if self.conf.c.getboolean('compliant archive store', 'enable',
                                      fallback=False):
                self._transferhcp(i[0], flist)

    def parsemanifest(self, manifest):
        """
        parse the manifest.csv and find the nodes IP addresses along with
        the compressed files holding its logs.

        :parm manifest:     the name of the manifest.csv file
        :returns:           a list of 3-tuples (containing the IP address,
                            path to the nodes compressed logs, path to
                            the logs when uncompressed)
        """
        self.logger.debug('parsing manifest for {}'
                          .format(self.tgtstr))
        with open(manifest, 'r') as mhdl:
            result = []
            relevant = False
            for l in mhdl.readlines():
                if l.startswith('"Node IP"'):
                    relevant = True
                    continue
                if not relevant:
                    continue
                else:
                    if not l.strip():
                        break
                    cols = l.split(',')
                    result.append((cols[0], cols[1],
                                   cols[1][:-8]))

        return result

    def _transferlocal(self, node, flist):
        """
        Transfer the unpacked files to local archive store
        :param flist:   a list of 2-tuples (source file, target path/name)
        :raises:        *HcplogsError*
        """
        self.logger.info('starting local transfer for node {} of {}'
                         .format(node, self.tgtstr))

        for s, d in flist:
            try:
                tgtpath = join(
                    self.conf.c.get('local archive store', 'path'),
                    self.tgt['folder'], d)
                makedirs(split(tgtpath)[0], exist_ok=True)
                copyfile(s, tgtpath)
            except Exception as e:
                self.logger.error(
                    'failed copying {}\n\thint: {}'.format(d, e))

        self.logger.debug('done: transfer for node {} of {}'
                          .format(node, self.tgt['fqdn']))

    def _transferhcp(self, node, flist):
        """
        Transfer the unpacked files to local archive store
        :param flist:   a list of 2-tuples (source file, target path/name)
        :raises:        *HcplogsError*
        """
        self.logger.info('starting compliance transfer for node {} of {}'
                         .format(node, self.tgtstr))

        adr = urlparse(self.conf.c.get('compliant archive store', 'path',
                                       fallback='None'))
        if not adr.netloc:
            raise hcplogs.HcplogError('[compliant archive store][path] lacks'
                                   'netloc')
        if not adr.scheme:
            raise hcplogs.HcplogError('[compliant archive store][path] lacks'
                                   'scheme')
        if adr.scheme == 'https':
            port = hcpsdk.P_HTTPS
        elif adr.scheme == 'http':
            port = hcpsdk.P_HTTP
        else:
            raise hcplogs.HcplogError('[compliant archive store][path] invalid'
                                   'scheme')

        auth = hcpsdk.NativeAuthorization(
            self.conf.c.get('compliant archive'
                            ' store',
                            'user',
                            fallback=''),
            self.conf.c.get('compliant archive'
                            ' store',
                            'password',
                            fallback=''))
        target = hcpsdk.Target(adr.netloc, auth, port=port)
        con = hcpsdk.Connection(target)

        for s, d in flist:
            tgtpath = '/'.join([adr.path, self.tgt['folder'], d])
            try:
                with open(s, 'rb') as shdl:
                    con.PUT(tgtpath, body=shdl,
                            params={'retention':
                                        self.conf.c.get('compliant archive '
                                                        'store',
                                                        'retention',
                                                        fallback='0')})
            except Exception as e:
                con.close()
                self.logger.error('failed ingesting {}\n'
                                  '\thint: {}'.format(d, e))
            else:
                status = con.response_status
                reason = con.response_reason
                if status not in [201, 409]:
                    self.logger.warning('ingest failed for {} ({}-{}'
                                        .format(self.tgt['fqdn'],
                                                status, reason))

        con.close()
        self.logger.debug('done: transfer for node {} of {}'
                          .format(node, self.tgt['fqdn']))

    def close(self):
        """
        Close the session with HCP
        """
        self.l.close()
        self.tmpdir.cleanup()
