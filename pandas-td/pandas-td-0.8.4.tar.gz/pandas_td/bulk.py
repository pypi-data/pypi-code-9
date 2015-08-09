class BulkUploader(object):
    def __init__(self, client, database, table):
        self.client = client
        self.database = database
        self.table = table

    def _chunk_frame(self, frame, chunksize):
        for i in range((len(frame) - 1) // chunksize + 1):
            yield frame[i * chunksize : i * chunksize + chunksize]

    def _pack(self, chunk):
        packer = msgpack.Packer(autoreset=False)
        for _, row in chunk.iterrows():
            record = dict(row)
            packer.pack(record)
        return packer.bytes()

    def _gzip(self, data):
        buff = io.BytesIO()
        with gzip.GzipFile(fileobj=buff, mode='wb') as f:
            f.write(data)
        return buff.getvalue()

    def _upload(self, data):
        data_size = len(data)
        unique_id = uuid.uuid4()
        elapsed = self.client.import_data(self.database, self.table, 'msgpack.gz', data, data_size, unique_id)
        logger.debug('imported %d bytes in %.3f secs', data_size, elapsed)

    def upload_frame(self, frame, chunksize):
        for chunk in self._chunk_frame(frame, chunksize):
            self._upload(self._gzip(self._pack(chunk)))

    def _prepare_file(self, file, format, **kwargs):
        fp = tempfile.TemporaryFile()
        with contextlib.closing(gzip.GzipFile(mode="wb", fileobj=fp)) as gz:
            packer = msgpack.Packer()
            with contextlib.closing(self._read_file(file, format, **kwargs)) as items:
                for item in items:
                    gz.write(packer.pack(item))
        fp.seek(0)
        return fp

