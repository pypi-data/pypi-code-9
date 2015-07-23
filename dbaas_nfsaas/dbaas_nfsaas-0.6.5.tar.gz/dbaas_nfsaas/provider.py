# -*- coding: utf-8 -*-
import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from client import NfsaasClient
from models import EnvironmentAttr, PlanAttr, HostAttr
from util import clean_unused_data
from time import sleep

LOG = logging.getLogger(__name__)


class NfsaasProvider(object):

    @classmethod
    def get_credentials(self, environment):
        LOG.info("Getting credentials...")
        from dbaas_credentials.credential import Credential
        from dbaas_credentials.models import CredentialType
        integration = CredentialType.objects.get(type=CredentialType.NFSAAS)

        return Credential.get_credentials(environment=environment, integration=integration)

    @classmethod
    def auth(self, environment, base_url=None):
        LOG.info("Conecting with nfsaas...")
        credentials = self.get_credentials(environment=environment)

        base_url = base_url or credentials.endpoint

        return NfsaasClient(baseurl=base_url,
                            username=credentials.user,
                            password=credentials.password)

    @classmethod
    @transaction.commit_on_success
    def grant_access(self, environment, host, export_id):

        LOG.info("Creating access!")

        nfsaas = self.auth(environment=environment)
        try:
            hostattrs = HostAttr.objects.get(nfsaas_export_id=export_id)
            nfsaas_team_id = hostattrs.nfsaas_team_id
            nfsaas_project_id = hostattrs.nfsaas_project_id
            nfsaas_environment_id = hostattrs.nfsaas_environment_id
            nfsaas_size_id = hostattrs.nfsaas_size_id
        except ObjectDoesNotExist as e:
            credentials = self.get_credentials(environment=environment)
            nfsaas_team_id = credentials.team
            nfsaas_project_id = credentials.project
            nfsaas_environment_id = EnvironmentAttr.objects.get(dbaas_environment=environment).nfsaas_environment
            plan = host.instance_set.all()[0].databaseinfra.plan
            nfsaas_size_id = PlanAttr.objects.get(dbaas_plan=plan).nfsaas_plan

        access = nfsaas.create_access(teamid=nfsaas_team_id,
                                      projectid=nfsaas_project_id,
                                      environmentid=nfsaas_environment_id,
                                      sizeid=nfsaas_size_id,
                                      exportid=export_id,
                                      host=host.address)

        LOG.info("Access created: %s" % access)

    @classmethod
    @transaction.commit_on_success
    def revoke_access(self, environment, host, export_id):

        LOG.info("Removing access on export (id=%s) from host %s" % (export_id, host))
        nfsaas = self.auth(environment=environment)
        hostattrs = HostAttr.objects.get(nfsaas_export_id=export_id)

        accesses = nfsaas.list_access(teamid=hostattrs.nfsaas_team_id,
                                      projectid=hostattrs.nfsaas_project_id,
                                      environmentid=hostattrs.nfsaas_environment_id,
                                      sizeid=hostattrs.nfsaas_size_id,
                                      exportid=export_id)

        for access in accesses:
            host_nfs = access["hosts"]
            host_network = nfsaas.change_ip(host.address)
            if host_nfs == host_network:
                LOG.info("Removing access on export (id=%s) from host %s" % (export_id, host))
                nfsaas.drop_access(teamid=hostattrs.nfsaas_team_id,
                                   projectid=hostattrs.nfsaas_project_id,
                                   environmentid=hostattrs.nfsaas_environment_id,
                                   sizeid=hostattrs.nfsaas_size_id,
                                   exportid=export_id,
                                   accessid=access['id'])
                LOG.info("Access deleted: %s" % access)
                break

    @classmethod
    @transaction.commit_on_success
    def create_disk(self, environment, plan, host):

        credentials = self.get_credentials(environment=environment)
        nfsaas = self.auth(environment=environment)
        nfsaas_planid = PlanAttr.objects.get(dbaas_plan=plan).nfsaas_plan
        nfsaas_environmentid = EnvironmentAttr.objects.get(dbaas_environment=environment).nfsaas_environment

        LOG.info("Creating export on environmen %s and size %s" % (nfsaas_environmentid, nfsaas_planid))
        export = nfsaas.create_export(teamid=credentials.team,
                                      projectid=credentials.project,
                                      environmentid=nfsaas_environmentid,
                                      sizeid=nfsaas_planid)
        LOG.info("Export created: %s" % export)

        LOG.info("Saving export info on nfsaas host attr")
        hostattr = HostAttr(host=host,
                            nfsaas_export_id=export['id'],
                            nfsaas_path=export['path'],
                            nfsaas_team_id=credentials.team,
                            nfsaas_project_id=credentials.project,
                            nfsaas_environment_id=nfsaas_environmentid,
                            nfsaas_size_id=nfsaas_planid)
        hostattr.save()

        LOG.info("Grant access on export")
        self.grant_access(environment, host, export['id'])

        return export

    @classmethod
    @transaction.commit_on_success
    def destroy_disk(self, environment, host):

        if not HostAttr.objects.filter(host=host).exists():
            LOG.info("There is no HostAttr for this host %s. It may be an arbiter." % (host))
            return True

        nfsaas = self.auth(environment=environment)
        deleted_exports = []

        hostattrs = HostAttr.objects.filter(host=host)

        databaseinfra = host.instance_set.all()[0].databaseinfra

        for hostattr in hostattrs:
            nfsaas_export_id = hostattr.nfsaas_export_id
            nfsaas_team_id = hostattr.nfsaas_team_id
            nfsaas_project_id = hostattr.nfsaas_project_id
            nfsaas_environment_id = hostattr.nfsaas_environment_id
            nfsaas_size_id = hostattr.nfsaas_size_id

            clean_unused_data(export_id=nfsaas_export_id,
                              export_path=hostattr.nfsaas_path,
                              host=host,
                              databaseinfra=databaseinfra,
                              provider=self)

            accesses = nfsaas.list_access(teamid=nfsaas_team_id,
                                          projectid=nfsaas_project_id,
                                          environmentid=nfsaas_environment_id,
                                          sizeid=nfsaas_size_id,
                                          exportid=nfsaas_export_id)

            for access in accesses:
                LOG.info("Removing access on export (id=%s) from host %s" % (nfsaas_export_id, host))
                nfsaas.drop_access(teamid=nfsaas_team_id,
                                   projectid=nfsaas_project_id,
                                   environmentid=nfsaas_environment_id,
                                   sizeid=nfsaas_size_id,
                                   exportid=nfsaas_export_id,
                                   accessid=access['id'])
                LOG.info("Access deleted: %s" % access)

            LOG.info("Deleting register from nfsaas host attr")
            hostattr.delete()

            try:
                LOG.info("Env: %s, size: %s, export: %s" % (nfsaas_environment_id,
                         nfsaas_size_id, nfsaas_export_id))
                deleted_export = nfsaas.drop_export(teamid=nfsaas_team_id,
                                                    projectid=nfsaas_project_id,
                                                    environmentid=nfsaas_environment_id,
                                                    sizeid=nfsaas_size_id,
                                                    exportid=nfsaas_export_id)
                LOG.info("Export deleted: %s" % deleted_export)
                deleted_exports.append(deleted_export)
            except Exception, e:
                LOG.error(str(e))
                return None

        return deleted_exports

    @classmethod
    def create_snapshot(self, environment, host):
        nfsaas = self.auth(environment=environment)

        hostattr = HostAttr.objects.get(host=host, is_active=True)

        snapshot = nfsaas.create_snapshot(teamid=hostattr.nfsaas_team_id,
                                          projectid=hostattr.nfsaas_project_id,
                                          environmentid=hostattr.nfsaas_environment_id,
                                          sizeid=hostattr.nfsaas_size_id,
                                          exportid=hostattr.nfsaas_export_id)

        return snapshot

    @classmethod
    def remove_snapshot(self, environment, host_attr, snapshot_id):
        nfsaas = self.auth(environment=environment)
        nfsaas.drop_snapshot(teamid=host_attr.nfsaas_team_id,
                             projectid=host_attr.nfsaas_project_id,
                             environmentid=host_attr.nfsaas_environment_id,
                             sizeid=host_attr.nfsaas_size_id,
                             exportid=host_attr.nfsaas_export_id,
                             snapshotid=snapshot_id)

    @classmethod
    def restore_snapshot(self, environment, export_id, snapshot_id):
        hostattr = HostAttr.objects.get(nfsaas_export_id=export_id)
        base_url = self.get_credentials(environment=environment).get_parameter_by_name('new_api_url')
        nfsaas = self.auth(environment=environment, base_url=base_url)
        return nfsaas.restore_snapshot(teamid=hostattr.nfsaas_team_id,
                                       projectid=hostattr.nfsaas_project_id,
                                       environmentid=hostattr.nfsaas_environment_id,
                                       sizeid=hostattr.nfsaas_size_id,
                                       exportid=export_id,
                                       snapshotid=snapshot_id)

    @classmethod
    def check_restore_nfsaas_job(self, environment, job_id,
                                 expected_status='finished', retries=50,
                                 interval=30):

        base_url = self.get_credentials(environment=environment).get_parameter_by_name('new_api_url')
        nfsaas = self.auth(environment=environment, base_url=base_url)
        nfsaas_environmentid = EnvironmentAttr.objects.get(dbaas_environment=environment).nfsaas_environment

        for attempt in range(retries):
            result = nfsaas.get_restore_job(base_url=base_url,
                                            environmentid=nfsaas_environmentid,
                                            job_id=job_id)

            if result.get('status') == expected_status:
                return result

            sleep(interval)

    @classmethod
    def drop_export(self, environment, export_id):
        nfsaas = self.auth(environment=environment)
        hostattr = HostAttr.objects.get(nfsaas_export_id=export_id)
        deleted_export = nfsaas.drop_export(teamid=hostattr.nfsaas_team_id,
                                            projectid=hostattr.nfsaas_project_id,
                                            environmentid=hostattr.nfsaas_environment_id,
                                            sizeid=hostattr.nfsaas_size_id,
                                            exportid=export_id)
        LOG.info("Export deleted: %s" % deleted_export)

        return deleted_export
