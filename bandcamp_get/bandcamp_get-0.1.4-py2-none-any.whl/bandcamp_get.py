#!/usr/bin/env python

#############################################################
#                                                           #
# bandcamp-get - automated music downloading via selenium   #
# written by Hunter Hammond (huntrar@gmail.com)             #
#                                                           #
#############################################################


import argparse as argp
import random
import time

import lxml.html as lh
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from . import __version__


USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) '
               'Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) '
               'Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) '
               'Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) '
               'AppleWebKit/536.5 (KHTML, like Gecko) '
               'Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) '
               'AppleWebKit/536.5 (KHTML, like Gecko) '
               'Chrome/19.0.1084.46 Safari/536.5')


def get_parser():
    parser = argp.ArgumentParser(description='automated music downloading\
                                              via selenium')
    parser.add_argument('user', metavar='USER', type=str, nargs='?',
                        help='bandcamp user to download from')
    parser.add_argument('-b', '--browser', type=str,
                        help='enter chrome or firefox, defaults to firefox')
    parser.add_argument('-e', '--email', type=str,
                        help='use your own email instead of a throwaway')
    parser.add_argument('-v', '--version', help='display current version',
                        action='store_true')
    return parser


def get_driver(browser):
    if browser and 'chrome' in browser.lower():
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent={}\
                             '.format(random.choice(USER_AGENTS)))
        return webdriver.Chrome(chrome_options=options)
    else:
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override\
                               ', random.choice(USER_AGENTS))
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'appl\
                               ication/zip')
        return webdriver.Firefox(profile)


def get_album_links(args):
    seed_url = 'https://{}.bandcamp.com'.format(args['user'])
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    request = requests.get(seed_url, headers=headers)
    html = lh.fromstring(request.text)
    all_links = html.xpath('//li/a[@href]/@href')
    album_links = []

    for link in all_links:
        if '/album/' in link:
            album_links.append(seed_url + link)
    return album_links


def auto_download(args):
    e_driver = get_driver(args['browser']) # Email driver
    e_driver.implicitly_wait(1)
    e_driver.get('https://www.guerrillamail.com/')
    args['email'] = e_driver.find_element_by_xpath('//span\
                                                   [@id="email-widget"]').text
    mail_cache = set()
    download(args)
    check_email(e_driver, mail_cache)

    ''' Check again in case of stragglers, will ignore duplicates '''
    e_driver.get('https://www.guerrillamail.com/')
    check_email(e_driver, mail_cache)
    try:
        e_driver.close()
    except Exception:
        pass


def check_email(e_driver, mail_cache):
    emails = e_driver.find_elements_by_xpath('//tbody[@id="email_list"]/tr')
    for mail in emails:
        download_mail_link(e_driver, mail_cache, mail)


def download_mail_link(e_driver, mail_cache, mail):
    mail_window = e_driver.window_handles[0]
    try:
        mail.click()
        try:
            dl_element = e_driver.find_element_by_xpath('//div[@class="\
                                                        email_body"]/div//a\
                                                        [@target="_blank"]')
            if dl_element.text not in mail_cache:
                mail_cache.add(dl_element.text)
                dl_element.click()
                dl_window = e_driver.window_handles[1]
                e_driver.switch_to_window(dl_window)

                e_driver.find_element_by_xpath('//a\
                                               [@class="downloadGo"]').click()
                e_driver.close()

                e_driver.switch_to_window(mail_window)
                e_driver.find_element_by_xpath('//a[@id="back_to\
                                               _inbox_link"]').click()
        except Exception:
            e_driver.switch_to_window(mail_window)
            e_driver.find_element_by_xpath('//a[@id="back_to\
                                           _inbox_link"]').click()
    except Exception:
        pass


def download(args):
    driver = get_driver(args['browser'])
    driver.implicitly_wait(1)
    for link in args['album_links']:
        if not download_link(args, driver, link):
            break
    try:
        driver.close()
    except Exception:
        pass


def download_link(args, driver, link):
    try:
        driver.get(link)
        driver.find_element_by_xpath("//button[@class='download-\
                                     link buy-link']").click()
    except Exception:
        return False

    print('Downloading {}'.format(link))
    try:
        element = driver.find_element_by_xpath('//input[@id="userPrice"]')
        element.send_keys('0')
        element.send_keys(Keys.RETURN)
    except Exception:
        pass

    try:
        element = driver.find_element_by_xpath('//input[@id="fan_\
                                               email_address"]')
        element.send_keys(args['email'])

        element = driver.find_element_by_id('fan_email_postalcode')
        element.send_keys(args['zip_code'])
        element.send_keys(Keys.RETURN)
    except Exception:
        pass

    try:
        driver.find_element_by_xpath('//a[@class="downloadGo"]').click()
        time.sleep(1)
    except Exception:
        pass

    return True


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if not args['user']:
        parser.print_help()
        return

    args['zip_code'] = random.randint(10000, 99999)
    args['album_links'] = get_album_links(args)
    if args['email']:
        download(args)
    else:
        auto_download(args)



if __name__ == '__main__':
    command_line_runner()
