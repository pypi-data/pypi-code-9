class BaseTopic(object):
    def __init__(self, name, producer_provider, consumer_provider):
        self.name = name
        self.producer_provider = producer_provider
        self.consumer_provider = consumer_provider

    def _unpack(self, message):
        raise NotImplementedError

    @property
    def producer(self):
        if not hasattr(self, '_producer'):
            self._producer = self.producer_provider()
        return self._producer

    @property
    def consumer(self):
        if not hasattr(self, '_consumer'):
            self._consumer = self.consumer_provider(self.name)
        return self._consumer

    def next(self):
        return self._unpack(self.consumer.next())

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def commit(self):
        self.consumer.commit()

    def task_done(self, message):
        self.consumer.task_done(message)


class Topic(BaseTopic):
    def __init__(self, name, producer_provider, consumer_provider, codec):
        super(Topic, self).__init__(name, producer_provider, consumer_provider)
        self.codec = codec

    def _unpack(self, message):
        return type(message)(
            message.topic,
            message.partition,
            message.offset,
            message.key,
            self.codec.decode(message.value))

    def send_messages(self, *messages):
        self.producer.send_messages(
            self.name,
            *[self.codec.encode(msg) for msg in messages])


class KeyedTopic(BaseTopic):
    def __init__(self, name, keyed_producer_provider, consumer_provider, key_codec, value_codec):
        super(KeyedTopic, self).__init__(name, keyed_producer_provider, consumer_provider)
        self.key_codec = key_codec
        self.value_codec = value_codec

    def send_messages(self, key, *messages):
        self.producer.send_messages(
            self.name,
            self.key_codec.encode(key),
            *[self.value_codec.encode(msg) for msg in messages])

    def _unpack(self, message):
        return type(message)(
            message.topic,
            message.partition,
            message.offset,
            self.key_codec.decode(message.key),
            self.value_codec.decode(message.value))
