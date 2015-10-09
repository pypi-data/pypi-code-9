import os
import platform
import argparse

from selenium import webdriver
from xvfbwrapper import Xvfb
import seleniumwrapper as selw
import selenium.webdriver.chrome.service as chrome_service


class Runner(object):
    def __init__(self, url, mobile=False):
        self.url = url
        self.mobile = mobile

    def start(self):
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'vendor',
            platform.system(),
            'chromedriver'
        )
        self.service = chrome_service.Service(path)
        self.service.start()

    def quit(self):
        self.driver.quit()

    def run_perf(self):
        chrome_options = webdriver.ChromeOptions()
        if self.mobile:
            chrome_options.add_experimental_option(
                "mobileEmulation",
                {"deviceName": "Google Nexus 5"}
            )

        capabilities = chrome_options.to_capabilities()
        self.driver = selw.connect('chrome', self.service.service_url, capabilities)
        self.driver.get(self.url)
        self.perf = self.driver.performance.timing

    def print_perf(self):
        self.result = {}
        base_line = self.perf.navigationStart
        self.result['domComplete'] = self.perf.domComplete - base_line
        self.result['domInteractive'] = self.perf.domInteractive - base_line
        self.result['domContentLoadedEventEnd'] = self.perf.domContentLoadedEventEnd - base_line
        print(self.result)


def main():
    parser = argparse.ArgumentParser(description='ThugPerf')
    parser.add_argument('url', help='url')
    parser.add_argument(
        '-m',
        '--mobile',
        dest='mobile',
        action='store_true',
        help='emulate mobile'
    )
    args = parser.parse_args()
    runner = Runner(url=args.url, mobile=args.mobile)
    with Xvfb(width=1280, height=720):
        runner.start()
        runner.run_perf()
        runner.print_perf()
        runner.quit()
