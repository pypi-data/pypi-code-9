from django.db import transaction, IntegrityError


def createIfNotExistsThreadSafe(modelClass, **fields):
    try:
        with transaction.atomic():
            return modelClass.objects.get_or_create(**fields)
    except IntegrityError as e:
        if e.args[0] != 1062:
            raise e


class ValidateOnSaveMixin:
    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)


class TransactionalSaveMixin:
    def save(self, **kwargs):
        with transaction.atomic():
            super().save(**kwargs)
