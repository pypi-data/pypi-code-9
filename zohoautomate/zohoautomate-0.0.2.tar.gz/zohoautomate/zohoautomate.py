# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

class ZohoAutomater:

    def __init__(self, username, password):
        self.browser_handle = self.load_zoho(username, password)

    # Boot Firefox, load Zoho and login. Store the browser handle for subsequent calls
    def load_zoho(self, username, password):
        browser = webdriver.Firefox()
        browser.get('https://www.zoho.com/mail/login.html')

        browser.switch_to.frame("zohoiam")

        userInputElement = browser.find_element_by_name("lid")
        userInputElement.send_keys(username)
        pwdInputElement = browser.find_element_by_name("pwd")
        pwdInputElement.send_keys(password)
        pwdInputElement.submit()

        time.sleep(15)

        return browser

    def check_contact_is_present(self, email):
        pass

    def add_contact_to_group(self, email, groupname):
        browser = self.browser_handle

        browser.get('https://contacts.zoho.com/home.zc')

        time.sleep(15)

        try:
            cancel_wizard = browser.find_element_by_link_text('Skip this step »')
        except NoSuchElementException as exc:
            pass
        else:
            cancel_wizard.click()

        contact_cbox = browser.find_element_by_xpath('''//dt[@title="{0}"]'''.format(email))
        contact_cbox.click()

        addtolist_button = browser.find_element_by_id('categoriesSpan')
        addtolist_button.click()

        add_to_group_item = browser.find_element_by_xpath('''//div[@categoryname="{0}"]'''.format(groupname))
        add_to_group_item.click()


    def add_contact_to_zoho(self, firstname, lastname, email):
        browser = self.browser_handle

        browser.get('https://contacts.zoho.com/home.zc')

        time.sleep(15)

        try:
            cancel_wizard = browser.find_element_by_link_text('Skip this step »')
        except NoSuchElementException as exc:
            pass
        else:
            cancel_wizard.click()

        addnew_button = browser.find_element_by_css_selector('.addnew > div:nth-child(1)')
        addnew_button.click()

        fname = browser.find_element_by_name('addFname')
        fname.send_keys(firstname)
        lname = browser.find_element_by_name('addLname')
        lname.send_keys(lastname)
        emailinput = browser.find_element_by_name('pmail')
        emailinput.send_keys(email)

        save_button = browser.find_element_by_css_selector('.contadd > div:nth-child(6) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)')
        save_button.click()

        time.sleep(5)
