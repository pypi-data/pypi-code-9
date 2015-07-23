# -*- coding: utf-8 -*-
import urllib2
import json


class NfsaasClient(object):

    def __init__(self, baseurl, username, password):

        self.base_url = baseurl
        self.username = username
        self.password = password

        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, self.base_url, self.username, self.password)
        handler = urllib2.HTTPBasicAuthHandler(p)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

    def create_export(self, teamid, projectid, environmentid, sizeid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/' % (
            self.base_url, teamid, projectid, environmentid, sizeid)
        request = urllib2.Request(url, data="{}")
        request.add_header("Content-Type", "application/json")
        newexport = json.load(urllib2.urlopen(request))
        newexport = json.loads(newexport[0])
        return newexport

    def drop_export(self, teamid, projectid, environmentid, sizeid, exportid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid)
        request = urllib2.Request(url)
        request.get_method = lambda: 'DELETE'
        deleted_export = urllib2.urlopen(request)
        return deleted_export

    def list_access(self, teamid, projectid, environmentid, sizeid, exportid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/acessos/' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid)
        return json.load(urllib2.urlopen(url))

    def change_ip(self, host):
        h = host.split('.')
        h = h[:len(h) - 1]
        return '.'.join(h) + '.0/24'

    def create_access(self, teamid, projectid, environmentid, sizeid, exportid, host):
        host = self.change_ip(host)
        accesses = self.list_access(teamid, projectid, environmentid, sizeid, exportid)
        for access in accesses:
            host_nfs = access["hosts"]
            if host_nfs == host:
                return access

        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/acessos/' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid)
        data = """{
            "hosts": "%s",
            "permission": {
                "type": "read-write"
            }
        }""" % (host,)
        request = urllib2.Request(url, data=data)
        request.add_header("Content-Type", "application/json")
        newaccess = json.load(urllib2.urlopen(request))
        newaccess = json.loads(newaccess[0])
        return newaccess

    def drop_access(self, teamid, projectid, environmentid, sizeid, exportid, accessid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/acessos/%s/' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid, accessid)
        request = urllib2.Request(url)
        request.get_method = lambda: 'DELETE'
        deleted_acesso = urllib2.urlopen(request)
        return deleted_acesso

    def list_snapshots(self, teamid, projectid, environmentid, sizeid, exportid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/snapshots/' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid)
        return json.load(urllib2.urlopen(url))

    def get_snapshot(self, teamid, projectid, environmentid, sizeid, exportid, snapshotid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/snapshots/%s/' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid, snapshotid)
        return json.load(urllib2.urlopen(url))

    def create_snapshot(self, teamid, projectid, environmentid, sizeid, exportid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/snapshots/' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid)
        request = urllib2.Request(url, data="{}")
        request.add_header("Content-Type", "application/json")
        return json.load(urllib2.urlopen(request))

    def drop_snapshot(self, teamid, projectid, environmentid, sizeid, exportid, snapshotid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/snapshots/%s/' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid, snapshotid)
        request = urllib2.Request(url)
        request.get_method = lambda: 'DELETE'
        deleted_export = urllib2.urlopen(request)
        return deleted_export

    def restore_snapshot(self, teamid, projectid, environmentid, sizeid, exportid, snapshotid):
        url = '%stimes/%s/projetos/%s/ambientes/%s/tamanhos/%s/exports/%s/snapshots/%s/restore' % (
            self.base_url, teamid, projectid, environmentid, sizeid, exportid, snapshotid)

        msg = "MyURL: {}".format(url)
        print(msg)

        request = urllib2.Request(url, data="{}")
        request.get_method = lambda: 'POST'

        request.add_header("Content-Type", "application/json")
        return json.load(urllib2.urlopen(request))

    def get_restore_job(self, base_url, environmentid, job_id):
        url = '%srestore/jobs/%s' % (base_url, job_id)

        msg = "MyURL: {}".format(url)
        print(msg)

        return json.load(urllib2.urlopen(url))
