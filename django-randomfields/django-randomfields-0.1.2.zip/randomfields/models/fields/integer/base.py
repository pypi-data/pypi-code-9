from django.core import checks
from django.db import models
from .... import random
from ..base import RandomFieldBase

class RandomIntegerFieldBase(RandomFieldBase):
    bytes = None
    lower_bound = None
    upper_bound = None
    
    def __init__(self, *args, **kwargs):
        super(RandomIntegerFieldBase, self).__init__(*args, **kwargs)
        
        if self.bytes is not None:
            self.bytes = int(self.bytes)
            
            if self.lower_bound is None and self.upper_bound is None:
                bit_exp = self.bytes * 8 - 1
                self.lower_bound = -(2 ** bit_exp)
                self.upper_bound = 2 ** bit_exp - 1
            else:
                raise TypeError("lower_bound and upper_bound must be None when bytes is specified")
            
        else:
            self.lower_bound = int(self.lower_bound)
            self.upper_bound = int(self.upper_bound)
            if self.upper_bound < self.lower_bound:
                raise ValueError("upper_bound may not be less than lower_bound")
        
        self.possibilities = self.upper_bound - self.lower_bound + 1
    
    def random(self):
        return random.randint(self.lower_bound, self.upper_bound)
    
    def formfield(self, **kwargs):
        defaults = {
            'min_value': self.lower_bound,
            'max_value': self.upper_bound,
        }
        defaults.update(kwargs)
        return super(RandomIntegerFieldBase, self).formfield(**defaults)

class RandomBigIntegerField(RandomIntegerFieldBase, models.BigIntegerField):
    bytes = 8

class RandomIntegerField(RandomIntegerFieldBase, models.IntegerField):
    bytes = 4

class RandomSmallIntegerField(RandomIntegerFieldBase, models.SmallIntegerField):
    bytes = 2

class RandomNarrowIntegerField(RandomIntegerFieldBase, models.IntegerField):
    """
        This field is a drop in replacement for AutoField primary keys.
        It returns a random integer between 1,000,000,000 and 2,147,483,647.
        These values were chosen specifically so that the string representation
        would be fixed length without requiring zero padding.
        
        This field uses a simpler approach to mimic the functionality of the
        identifier fields like `RandomBigIntegerIdentifierField`,
        `RandomIntegerIdentifierField`, and `RandomSmallIntegerIdentifierField`
        which cannot be reliably implemented under older versions of Django (< 1.8)
        due to lack of Field.from_db_value() support.
    """
    lower_bound = 1000000000
    upper_bound = 2147483647

class NarrowPositiveIntegerField(RandomNarrowIntegerField):
    def check(self, **kwargs):
        errors = super(NarrowPositiveIntegerField, self).check(**kwargs)
        errors.append(checks.Warning(
            'NarrowPositiveIntegerField has been deprecated.',
            hint='Use RandomNarrowIntegerField instead.',
            obj=self,
            id='%s.%s.Depreciated' % (__name__, self.__class__.__name__),
        ))
        return errors
