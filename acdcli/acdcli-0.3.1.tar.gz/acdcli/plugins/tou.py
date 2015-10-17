from . import *

TOU_URL = 'https://www.amazon.com/gp/help/customer/display.html/?ie=UTF8&nodeId=201376540'


class TermsOfUsePlugin(Plugin):
    MIN_VERSION = '0.1.3'

    @classmethod
    def attach(cls, subparsers: argparse.ArgumentParser, log: list, **kwargs):
        p = subparsers.add_parser('tou', add_help=False)
        p.set_defaults(func=cls.action)
        log.append(str(cls) + ' attached.')

    @staticmethod
    def action(args: argparse.Namespace) -> int:
        import requests
        from bs4 import BeautifulSoup

        r = requests.get(TOU_URL)
        tou = BeautifulSoup(r.text)
        div = tou.h1.find_next('div')
        print(div.get_text())

        return 0
