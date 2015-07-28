from celery.task import task

from .client import MonomailClient

@task
def task_send_from_template( toemail, subject, template, context = {} ):
    """Celery Task to Send From Template"""
    c = MonomailClient()
    c.send_from_template( toemail, subject, template, context )
    
@task
def task_send_from_model( toemail, txtid, context ):
    """Celery Task to Send From Model"""
    c = MonomailClient()
    c.send_from_model( toemail, txtid, context )