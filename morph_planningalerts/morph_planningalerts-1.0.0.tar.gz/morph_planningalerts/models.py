from datetime import date
from peewee import (
    SqliteDatabase, Model, CharField, DateField
)

__all__ = [
    'DevelopmentApplication',
    'MorphDatabase'
]

database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class DevelopmentApplication(BaseModel):
    """ Expected fields of one development application.

    As per specs at: https://www.planningalerts.org.au/how_to_write_a_scraper
    """

    class Meta:
        db_table = 'data'

    # Required fields...
    council_reference = CharField(unique=True, null=False, index=True)
    address = CharField(null=False)
    description = CharField(null=False)
    info_url = CharField(null=False)
    comment_url = CharField(null=False)
    date_scraped = DateField(default=date.today(), null=False)

    # Optionals...
    date_received = DateField(null=True)
    on_notice_from = DateField(null=True)
    on_notice_to = DateField(null=True)


class MorphDatabase:
    @classmethod
    def init(cls, db_path=None):
        global database
        database.init(db_path or "data.sqlite")
        database.connect()
        database.create_tables([DevelopmentApplication], safe=True)

    @classmethod
    def close(cls):
        global database
        database.close()
        database = SqliteDatabase(None)
