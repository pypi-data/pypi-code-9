import urllib
import json
import urllib.request

class KassisNumbering:
    def numbering(identifier, service_server_url = None):
        default_service_server = "http://localhost:59630"
        numbering_prefix = "/numbering/"

        service_server_url = service_server_url or default_service_server
        service_url = "{0}{1}{2}".format(service_server_url, numbering_prefix, identifier)

        try:
            response = urllib.request.urlopen(service_url)
            results = response.read()
            response.close()
            jsonData = json.loads(results.decode('utf-8'))
        except Exception as e:
            print("Connection error")
            print(e)
            return None

        return jsonData.get("v", None)

if "__main__" == __name__:
    v = v0 = KassisNumbering.numbering("M")
    assert v != None
    v = KassisNumbering.numbering("M")
    assert int(v) == (int(v0) + 1)
    assert KassisNumbering.numbering("U") != None
    assert KassisNumbering.numbering("X") == None
    assert KassisNumbering.numbering("U", "http://localhost:59630") != None
    assert KassisNumbering.numbering("U", "http://localhost:9999") == None
