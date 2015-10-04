from django.db import models

class Employee(models.Model):
    '''
    Employee Information model
    '''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%s, %s' % (self.first_name, self.last_name)

class SystemSetting(models.Model):
    '''
    System Setting model
    '''
    name = models.CharField(max_length=10)
    value = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s, %s' % (self.name, self.value)
