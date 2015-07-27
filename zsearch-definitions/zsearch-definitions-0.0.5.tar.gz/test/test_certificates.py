import json
import test.testcase
import time

class CertificateTests(test.testcase.ZDBTestCase):

    def add_mock_certificates(self):
        certs = json.loads(open("test/certificates.json").read())
        for cert in certs:
            self.query_grpc.put_certificate(cert["raw"], cert["parsed"])

    def test_certificate_dump(self):
        time.sleep(3)
        self.add_mock_certificates()
        self.admin_grpc.dump_certificates(path="certificates.json", incremental=False)