import os
import platform
import argparse

from selenium import webdriver
from xvfbwrapper import Xvfb
import seleniumwrapper as selw
import selenium.webdriver.chrome.service as chrome_service


class Runner(object):
    def __init__(self, url, runs, mobile=False):
        self.url = url
        self.mobile = mobile
        self.runs = runs
        self.results = {
            'domComplete': [],
            'domInteractive': [],
            'domContentLoadedEventEnd': []
        }

    def start(self):
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'vendor',
            platform.system(),
            'chromedriver'
        )
        self.service = chrome_service.Service(path)
        self.service.start()

    def run_perf(self):
        chrome_options = webdriver.ChromeOptions()
        if self.mobile:
            chrome_options.add_experimental_option(
                "mobileEmulation",
                {"deviceName": "Google Nexus 5"}
            )

        capabilities = chrome_options.to_capabilities()

        for run in range(self.runs):
            driver = selw.connect('chrome', self.service.service_url, capabilities)
            driver.get(self.url)
            self.store_perf(driver.performance.timing)
            driver.quit()

    def store_perf(self, perf):
        base_line = perf.navigationStart

        self.results['domComplete'].\
            append(perf.domComplete - base_line)
        self.results['domInteractive'].\
            append(perf.domInteractive - base_line)
        self.results['domContentLoadedEventEnd'].\
            append(perf.domContentLoadedEventEnd - base_line)

    def print_perf(self):
        print("%s:" % self.url)
        for k, v in self.results.iteritems():
            result = reduce(lambda x, y: x + y, v) / len(v)
            print("%s - %ims" % (k, result))


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
    parser.add_argument(
        '-r',
        '--repetions',
        type=int,
        help='Number of runs'
    )
    args = parser.parse_args()
    runner = Runner(url=args.url, runs=args.repetions, mobile=args.mobile)
    with Xvfb(width=1280, height=720):
        runner.start()
        runner.run_perf()
        runner.print_perf()
