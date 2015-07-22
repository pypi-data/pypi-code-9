
from .yajl.parse import YajlParser, YajlListener
from .tape import Tape

json_input = """[
      {
        "_id": "54926f0437ecbc6d8312303b",
        "index": 0,
        "aware":true,
        "double":74.5,
        "guid": "e43742fa-6195-4722-a0ea-498f668025e0",
        "isActive": false,
        "balance": "$3,103.04",
        "picture": "http://placehold.it/32x32",
        "age": 32,
        "eyeColor": "green",
        "name": "Ann Hyde",
        "gender": "female",
        "company": "DARWINIUM",
        "email": "annhyde@darwinium.com",
        "phone": "+1 (869) 421-3562",
        "address": "812 Ferris Street, Calvary, Louisiana, 6032",
        "about": "Commodo eu laboris sint nostrud et deserunt minim amet. Aliquip exercitation nulla mollit proident velit id velit laboris fugiat. Aliqua deserunt dolore nostrud id proident exercitation excepteur Lorem non reprehenderit. Tempor sit et occaecat non est proident voluptate aliqua esse. Pariatur pariatur nostrud mollit magna sit nostrud duis cillum consectetur proident ipsum Lorem esse. Officia eiusmod non voluptate ad excepteur reprehenderit ullamco adipisicing magna eu proident voluptate.\\r\\n",
        "registered": "2014-10-26T11:04:19 -06:-30",
        "latitude": 8.175509,
        "longitude": 5.955378,
        "tags": [
          "sunt",
          "eiusmod",
          "magna",
          "ex",
          "ipsum",
          "amet",
          "fugiat"
        ],
        "friends": [
          {
            "id": 0,
            "name": "Annabelle Gibson"
          },
          {
            "id": 1,
            "name": "Faith Gutierrez"
          },
          {
            "id": 2,
            "name": "Thompson Black"
          }
        ],
        "greeting": "Hello, Ann Hyde! You have 6 unread messages.",
        "favoriteFruit": "strawberry"
      },
      {
        "_id": "54926f0407dd6e36bc016ab7",
        "index": 1,
        "guid": "9201a165-cc39-45ae-b1ed-339db74e0850",
        "isActive": false,
        "balance": "$1,582.94",
        "picture": "http://placehold.it/32x32",
        "age": 31,
        "eyeColor": "brown",
        "name": "Odessa Cleveland",
        "gender": "female",
        "company": "SOFTMICRO",
        "email": "odessacleveland@softmicro.com",
        "phone": "+1 (870) 488-3607",
        "address": "736 Nautilus Avenue, Clarksburg, Federated States Of Micronesia, 7789",
        "about": "Aliqua esse magna irure proident laboris magna laborum excepteur amet eu veniam. Nulla in reprehenderit veniam deserunt voluptate ex ipsum eu cillum mollit tempor culpa labore magna. Veniam aliquip mollit elit reprehenderit.\\r\\n",
        "registered": "2014-08-11T19:05:24 -06:-30",
        "latitude": 64.104772,
        "longitude": -127.211982,
        "tags": [
          "exercitation",
          "officia",
          "aliqua",
          "velit",
          "sit",
          "reprehenderit",
          "est"
        ],
        "friends": [
          {
            "id": 0,
            "name": "Elise Giles"
          },
          {
            "id": 1,
            "name": "Blanche Lynch"
          },
          {
            "id": 2,
            "name": "Elma Perry"
          }
        ],
        "greeting": "Hello, Odessa Cleveland! You have 10 unread messages.",
        "favoriteFruit": "apple"
      },
      {
        "_id": "54926f04911a99ae145b3590",
        "index": 2,
        "guid": "402cffef-54bc-4640-9079-51ab02af913e",
        "isActive": false,
        "balance": "$2,394.92",
        "picture": "http://placehold.it/32x32",
        "age": 27,
        "eyeColor": "blue",
        "name": "Cabrera Burnett",
        "gender": "male",
        "company": "ZILCH",
        "email": "cabreraburnett@zilch.com",
        "phone": "+1 (865) 466-3885",
        "address": "769 Franklin Street, Groton, Michigan, 9636",
        "about": "Aliqua ex labore labore dolore adipisicing sunt ut veniam aute ut aliquip. Amet nisi eu aliquip qui eu enim duis proident magna. Nulla veniam magna excepteur dolore laborum fugiat do consequat in ea elit deserunt. Ex culpa laboris velit occaecat officia commodo velit reprehenderit nisi consequat esse culpa. In deserunt in culpa do.\\r\\n",
        "registered": "2014-07-04T12:51:22 -06:-30",
        "latitude": 10.022683,
        "longitude": -153.137929,
        "tags": [
          "laborum",
          "consequat",
          "fugiat",
          "Lorem",
          "officia",
          "et",
          "est"
        ],
        "friends": [
          {
            "id": 0,
            "name": "Shawna Webster"
          },
          {
            "id": 1,
            "name": "Snider Morrison"
          },
          {
            "id": 2,
            "name": "Marsha Martinez"
          }
        ],
        "greeting": "Hello, Cabrera Burnett! You have 2 unread messages.",
        "favoriteFruit": "banana"
      }
    ]
    """


class MyListener(YajlListener):
  def on_null(self, ctx):
    print("null\n" )
  def on_boolean(self, ctx, boolVal):
    print('type', type(boolVal))
    print("bool: %s\n" %('true' if boolVal else 'false'))
  def on_number(self, ctx, stringNum):
    ''' Since this is defined both integer and double callbacks are useless '''
    print('type', type(stringNum))
    num = float(stringNum) if '.' in stringNum else int(stringNum)
    print("number: %s\n" %num)
  def on_string(self, ctx, stringVal):
    print("string: '%s'\n" %stringVal)
  def on_start_map(self, ctx):
    print("map open '{'\n")
  def on_map_key(self, ctx, stringVal):
    print("key: '%s'\n" %stringVal)
  def on_end_map(self, ctx):
    print("map close '}'\n")
  def on_start_array(self, ctx):
    print("array open '['\n")
  def on_end_array(self, ctx):
    print("array close ']'\n")



def main():
  parser = YajlParser(MyListener())
  parser.parse(Tape(json_input))



if __name__ == '__main__':
    main()