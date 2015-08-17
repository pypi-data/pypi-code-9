from avro_codec import AvroCodec


class RegisteredSchemaAvroCodec(object):
    """
    Avro codec which ensure the schema associated with the
    instance is present in a confluent schema registry.
    """

    def __init__(self, topic_name, schema, registry_provider):
        self.registry_provider = registry_provider
        self.schema = schema
        self.topic_name = topic_name
        self._encode_codec = None
        self._decode_codec = None

    @property
    def registry(self):
        if not hasattr(self, '_registry'):
            self._registry = self.registry_provider()
        return self._registry

    @property
    def encode_codec(self):
        # The first time we attempt to encode, make sure the schema is
        # registered with the schema registry before returning the
        # codec based on the schema. This will ensure we aren't writing
        # data using a borked schema.
        if not self._encode_codec:
            self.registry.register_subject_version(self.topic_name, self.schema)
            self._encode_codec = AvroCodec(self.schema)
        return self._encode_codec

    @property
    def decode_codec(self):
        # Build the decode codec from the schema registered against the
        # topic we've been setup with.
        if not self._decode_codec:
            self._decode_codec = AvroCodec(self.registry.get_subject_latest_version(self.topic_name))
        return self._decode_codec

    def encode(self, data):
        return self.encode_codec.dumps(data)

    def decode(self, data):
        return self.decode_codec.loads(data)
