from yowsup.layers import YowLayer
import peewee
db = None
class SqliteStorageLayer(YowLayer):
    pass

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Contact(BaseModel):
    phone = peewee.CharField(unique=True)
    picture = peewee.BlobField()