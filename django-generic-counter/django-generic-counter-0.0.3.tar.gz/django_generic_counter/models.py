from django.db import models


class Counter(models.Model):
    """
    A simple counter which can be used to store a count of anything.
    """
    name = models.CharField(max_length=128)
    count = models.IntegerField(default=0)

    def __iadd__(self, other):
        """
        Use the database to increment the counter atomically.
        """
        cls = type(self)
        cls.objects.filter(pk=self.pk).update(
            count=models.F("count")+other)
        self.count = cls.objects.get(pk=self.pk).count
        return self

    def __isub__(self, other):
        """
        Use the database to decrement the counter atomically.
        """
        cls = type(self)
        cls.objects.filter(pk=self.pk).update(
            count=models.F("count")-other)
        self.count = cls.objects.get(pk=self.pk).count
        return self

    def __int__(self):
        """
        Enable casting to int to display the counter value.
        """
        return self.count
