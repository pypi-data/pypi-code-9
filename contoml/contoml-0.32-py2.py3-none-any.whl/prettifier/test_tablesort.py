import contoml
from contoml.prettifier import tablesort


def test_table_sorting():
    toml_text = """description = ""
firstname = "adnan"
lastname = "fatayerji"
git_aydo = ""
groups = ["sales", "dubai", "mgmt"]
skype = ""
emails = ["adnan@incubaid.com",
 "fatayera@incubaid.com",
 "adnan.fatayerji@incubaid.com",
 "adnan@greenitglobe.com",
 "fatayera@greenitglobe.com",
 "adnan.fatayerji@greenitglobe.com"]
# I really like this table
id = "fatayera"
git_github = ""
telegram = "971507192009"
mobiles = ["971507192009"]
"""

    prettified = """description = ""
emails = ["adnan@incubaid.com",
 "fatayera@incubaid.com",
 "adnan.fatayerji@incubaid.com",
 "adnan@greenitglobe.com",
 "fatayera@greenitglobe.com",
 "adnan.fatayerji@greenitglobe.com"]
firstname = "adnan"
git_aydo = ""
git_github = ""
groups = ["sales", "dubai", "mgmt"]
# I really like this table
id = "fatayera"
lastname = "fatayerji"
mobiles = ["971507192009"]
skype = ""
telegram = "971507192009"
"""

    f = contoml.loads(toml_text)
    print(f.dumps())
    f.prettify(prettifiers=[tablesort.sort_table_entries])

    assert prettified == f.dumps()
