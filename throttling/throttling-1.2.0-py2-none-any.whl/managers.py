#!/usr/bin/env python
# encoding: utf-8
from django.db import models
from django.db.models import Min
from django.db.models import Sum

class AccessQuerySet(models.QuerySet):
    
    def anonymous(self):
        return self.filter(consumer__ip__isnull=False)
        
    def count_requests(self):
        return self.aggregate(count=Sum('count'))['count']
        
    def min_datemark(self):
        return self.aggregate(min_date=Min('datemark'))['min_date']
