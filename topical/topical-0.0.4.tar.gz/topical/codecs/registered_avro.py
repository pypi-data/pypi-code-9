from avro_codec import AvroCodec


class RegisteredSchemaAvroCodec(object):
    """
    Avro codec which ensure the schema associated with the
    instance is present in a confluent schema registry.
    """

    def __init__(self, topic_name, schema, registry_provider):
        self.registry = registry_provider()
        self.schema = schema
        self.topic_name = topic_name
        self.inner_codec = AvroCodec(schema)
        self.synced = False

    def sync_if_required(self):
        if not self.synced:
            self.registry.register_subject_version(self.topic_name, self.schema)
            self.synced = True

    def encode(self, data):
        self.sync_if_required()
        return self.inner_codec.dumps(data)

    def decode(self, data):
        self.sync_if_required()
        return self.inner_codec.loads(data)
