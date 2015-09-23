import requests
from bs4 import BeautifulSoup
import datetime
import random


class Checkerproxy(object):
    def __init__(self,
                 user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36",
                 date = datetime.datetime.now()):
        """
        :type date: datetime.datetime
        :type user_agent: str
        :rtype : None
        :param user_agent: User agent used to request the proxies from http://checkerproxy.net
        :param date: Get active proxies from that date
        """
        self.user_agent = user_agent

        self.html = requests.get(
            "http://checkerproxy.net/getProxy?date=" + date.now().strftime("%Y-%-m-%d"),
            headers = {"User-Agent": self.user_agent}).content
        self.soup = BeautifulSoup(self.html, "lxml")

        self.proxies = [proxy.text for proxy in self.soup.find("div", {"class": "block archive full_list"}).find("ul").find_all("li")]

    @property
    def proxies_requests_form(self):
        """
        :rtype : list
        """
        """A list of dictionaries used by the request module to declare proxies, for example {"http": "127.0.0.1"}"""
        return [{"http": proxy} for proxy in self.proxies]

    def random_proxy(self):
        return random.choice(self.proxies)
    