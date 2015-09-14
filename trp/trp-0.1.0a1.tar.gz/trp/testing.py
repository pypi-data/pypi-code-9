from trp import TRP

t = TRP("../../ontrac/src/secrets.json")
t.scraper.extract(66, "person")
t.exit()
