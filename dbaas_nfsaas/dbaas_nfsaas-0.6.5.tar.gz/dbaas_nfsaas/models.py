# -*- coding: utf-8 -*-
from util.models import BaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _
from backup.models import Snapshot


class EnvironmentAttr(BaseModel):
    dbaas_environment = models.ForeignKey(
        'physical.Environment', related_name="nfsaas_environment_attributes")
    nfsaas_environment = models.CharField(
        verbose_name=_("Environment ID"), max_length=10)

    class Meta:
        verbose_name_plural = 'NFaaS Custom Environment Attributes'


class PlanAttr(BaseModel):
    dbaas_plan = models.ForeignKey(
        'physical.Plan', related_name="nfsaas_plan_attributes")
    nfsaas_plan = models.CharField(verbose_name=_("Plan ID"), max_length=10)

    class Meta:
        verbose_name_plural = 'NFaaS Custom Plan Attributes'


class HostAttr(BaseModel):
    host = models.ForeignKey('physical.Host', related_name="nfsaas_host_attributes")
    nfsaas_export_id = models.CharField(verbose_name=_("Export ID"), max_length=10)
    nfsaas_path = models.CharField(verbose_name=_("Path"), max_length=100)
    is_active = models.BooleanField(verbose_name=_("Is instance active"), default=True)
    nfsaas_team_id = models.CharField(verbose_name=_("Team ID"), max_length=10)
    nfsaas_project_id = models.CharField(verbose_name=_("Project ID"), max_length=10)
    nfsaas_environment_id = models.CharField(verbose_name=_("Environment ID"), max_length=10)
    nfsaas_size_id = models.CharField(verbose_name=_("Size ID"), max_length=10)

    class Meta:
        verbose_name_plural = 'NFaaS Custom Host Attributes'

    def snapshots(self,):
        return Snapshot.objects.filter(export_path=self.nfsaas_path,
                                       purge_at=None)
