
import models
from xwot.util.annotator import Annotator
from xwot.util.serializer import Serializer
from xwot.util import local_ip
annotator = Annotator()


serializer = Serializer(annotator)

entrypoint = models.EntryPoint()

url = "http://%s:%s" % (local_ip(), 3000)
output = serializer.serialize(entrypoint, content_type='text/html')

print(output)
