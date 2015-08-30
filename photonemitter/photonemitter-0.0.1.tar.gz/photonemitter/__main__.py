import photonemitter
from . import config
from . import output


def main():
    cfg = config.Configuration()
    ps = photonemitter.ProviderSet()
    for prov in cfg.providers:
        ps.add(**prov)

    while True:
        line = input()
        results = ps.query(line)
        if results is None:
            print()
        else:
            output.send(results)


main()
