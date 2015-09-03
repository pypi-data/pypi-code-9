#encoding:utf-8
from django.test import TestCase
from microsip_api.comun.sic_db import first_or_none
from datetime import datetime, timedelta
from . import models


class ProgrammedTaskTests(TestCase):
    def setUp(self):
        models.ProgrammedTask.objects.all().delete()
        models.ProgrammedTask.objects.create(
            description='Mail Saldos Automaticos',
            command_type='http',
            command='http://127.0.0.1:8001/mail/saldos/todos_automatico/',
            period_start_datetime=datetime.now(),
            period_quantity=1,
            period_unit='dia',
        )

    def test_progremmedtask_is_created(self):
        task = first_or_none(models.ProgrammedTask.objects.filter(description='Mail Saldos Automaticos'))
        self.assertIsNotNone(task, msg='No se encontro la tarea por crear')

    def test_next_execution_is_not_none(self):
        task = first_or_none(models.ProgrammedTask.objects.filter(description='Mail Saldos Automaticos'))
        self.assertIsNotNone(task.next_execution, msg='No se calcula la siguiente ejecucion al crear la tarea')

    # def test_next_execution_is_lessthan_end_datetime(self):
    #     """
    #     Checar que si se guarda una tarea no se guarde nunca
    #     fechahora de siguiente ejecucion mayor a la fecha de fin.
    #     """
    #     task = first_or_none(models.ProgrammedTask.objects.filter(description='Mail Saldos Automaticos'))
    #     task.period_end_datetime = task.period_start_datetime + timedelta(days=1)
    #     task.save()
    #     if task.period_end_datetime:
    #         self.assertTrue(task.next_execution < task.period_end_datetime, msg='La siguiente ejecucion se esta guardando con fecha posterior a la fecha de fin')
