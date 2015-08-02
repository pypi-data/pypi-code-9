from TextSharer import TextSharer
import requests

class SprungeSharer(TextSharer):
    def __init__(self):
        super(SprungeSharer, self).__init__("SprungeSharer")

    def uploadtext(self, text):
        res = requests.post("http://sprunge.us", params={"sprunge":text})
        if res.status_code == 200:
            self.uploadSuccess = True
            return res.text.rstrip("\r\n")
        else:
            self.uploadSuccess = False
            return "Something is wrong please report it in https://github.com/bindingofisaac/textshare\n"
