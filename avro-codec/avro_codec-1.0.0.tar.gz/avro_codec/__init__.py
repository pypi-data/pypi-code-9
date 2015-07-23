import avro.schema
import json
from avro.io import DatumReader, DatumWriter, BinaryEncoder, BinaryDecoder
from io import BytesIO


class AvroCodec(object):
    def __init__(self, schema):
        self._schema = avro.schema.parse(json.dumps(schema))
        self._writer = DatumWriter(self._schema)
        self._reader = DatumReader(self._schema)

    def dump(self, obj, fp):
        """
        Serializes obj as an avro-format byte stream to the provided
        fp file-like object stream.
        """
        self._writer.write(obj, BinaryEncoder(fp))

    def dumps(self, obj):
        """
        Serializes obj to an avro-format byte array and returns it.
        """
        out = BytesIO()
        try:
            self.dump(obj, out)
            return out.getvalue()
        finally:
            out.close()

    def load(self, fp):
        """
        Deserializes the byte stream contents of the given file-like
        object into an object and returns it.
        """
        return self._reader.read(BinaryDecoder(fp))

    def loads(self, data):
        """
        Deserializes the given byte array into an object and returns it.
        """
        st = BytesIO(data)
        try:
            return self.load(st)
        finally:
            st.close()
