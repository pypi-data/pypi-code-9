from spex.artifact_server import ArtifactServer
from tornado.httpclient import HTTPClient

TEST_DATA = {
   'test_file.txt': 'This is a test file',
   'test_file2.txt': 'This is another test file'
}

def test_artifact_server(tmpdir, thread_leak_checker):
    with ArtifactServer(str(tmpdir.realpath())) as artifact_server:
        for name, data in TEST_DATA.items():
            test_file = tmpdir.join(name)
            test_file.write(data)

            artifact_uri = artifact_server.artifact_uri_resolver()(name)

            httpclient = HTTPClient()
            response = httpclient.fetch(artifact_uri)

            assert response.code == 200
            assert response.body == data
