from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from xvfbwrapper import Xvfb
from getpass import getpass


class Firefox:

    login_url = 'https://accounts.google.com/login'
    hangout_url = 'https://hangouts.google.com/'

    def __init__(self):
        self.vdisplay = Xvfb()
        self.vdisplay.start()
        self.b = webdriver.Firefox()
        self.get = self.b.get
        self.raw = self.b.page_source
        self.chat_status = False
        self.retry_chances = 20
        self.login()

    def __del__(self):
        self.b.close()
        self.vdisplay.stop()

    def sel(self, path, engine='css'):
        retry_times = 0
        while True:
            try:
                if retry_times < self.retry_chances:
                    sleep(0.1)
                    if engine == 'css':
                        ele = self.b.find_element_by_css_selector(path)
                    elif engine == 'xpath':
                        ele = self.b.find_element_by_xpath(path)
                    sleep(0.1)
                    return ele
                else:
                    raise Exception('No more chance to retry (retry times: %d)' % retry_times)
            except:
                print('retry times: %d' % retry_times)
                retry_times += 1

    def login(self):
        account = input('Account: ')
        password = getpass('Password: ')
        self.get(self.login_url)
        self.sel('#Email').send_keys(account)
        self.sel('#Email').send_keys(Keys.RETURN)
        sleep(2)
        self.sel('#Passwd').send_keys(password)
        self.sel('#Passwd').send_keys(Keys.RETURN)
        sleep(4)

    def chat(self, message):
        if not self.chat_status:
            self.get(self.hangout_url)
            ele = self.sel('#gtn-roster-iframe-id-b')
            self.b.switch_to_frame(ele)
            self.sel('//span[text()="amigcamel"]', 'xpath').click()
            self.b.switch_to_default_content()
            chat_iframe = self.sel('.talk_chat_widget > iframe')
            self.b.switch_to_frame(chat_iframe)
            # click dialog box
            self.sel('//span[text()="Send a message"]', 'xpath').click()
            self.chat_status = True
        self.sel('div[contenteditable="true"]').send_keys(message)
        self.sel('div[contenteditable="true"]').send_keys(Keys.RETURN)
