import uuid
from uuid import UUID
from unittest import TestCase
from nssjson.compat import StringIO, reload_module

import nssjson as json

class TestUuid(TestCase):
    UUIDs = 'a'*32, '0'*31 + '1'

    def dumps(self, obj, **kw):
        sio = StringIO()
        json.dump(obj, sio, **kw)
        res = json.dumps(obj, **kw)
        self.assertEqual(res, sio.getvalue())
        return res

    def loads(self, s, **kw):
        sio = StringIO(s)
        res = json.loads(s, **kw)
        self.assertEqual(res, json.load(sio, **kw))
        return res

    def test_uuid_encode(self):
        for u in map(UUID, self.UUIDs):
            self.assertEqual(self.dumps(u, handle_uuid=True), '"%s"' % str(u))

    def test_uuid_decode(self):
        for u in map(UUID, self.UUIDs):
            self.assertEqual(self.loads('"%s"' % str(u), handle_uuid=True), u)

    def test_stringify_key(self):
        for u in map(UUID, self.UUIDs):
            v = {u: u}
            self.assertEqual(
                self.loads(self.dumps(v, handle_uuid=True), handle_uuid=True), v)

    def test_uuid_roundtrip(self):
        for u in map(UUID, self.UUIDs):
            for v in [u, [u], {'': u}]:
                self.assertEqual(
                    self.loads(self.dumps(v, handle_uuid=True), handle_uuid=True), v)

    def test_uuid_defaults(self):
        u = UUID(int=42)
        # handle_uuid=False is the default
        self.assertRaises(TypeError, json.dumps, u)
        self.assertEqual('"%s"' % u, json.dumps(u, handle_uuid=True))
        self.assertRaises(TypeError, json.dump, u, StringIO())

    def test_uuid_reload(self):
        # Simulate a subinterpreter that reloads the Python modules but not
        # the C code https://github.com/simplejson/simplejson/issues/34
        global UUID
        UUID = reload_module(uuid).UUID
        import nssjson.encoder
        nssjson.encoder.UUID = UUID
        self.test_uuid_roundtrip()
