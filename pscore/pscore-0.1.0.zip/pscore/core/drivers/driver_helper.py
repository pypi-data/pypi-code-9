import os
import urllib
import zipfile

import requests


class DriverHelper(object):
    @staticmethod
    def download_destination(folder_name):
        if DriverHelper.os_name() is 'win':
            home = 'HOMEPATH'
        elif DriverHelper.os_name() is 'mac':
            home = 'HOME'
        else:
            raise NotImplemented('Home path for os is not implemented yet')

        homepath = os.getenv(home)
        driver_path = os.path.join(homepath, folder_name)
        if not os.path.exists(driver_path):
            os.mkdir(driver_path)

        return driver_path

    @staticmethod
    def os_name():
        name = os.name
        if name is 'nt':
            return 'win'
        elif name is 'posix':
            return 'mac'
        else:
            raise NotImplemented("Downloading chrome for {} has not been implemented yet".format(name))


class IEDriverHelper(object):
    IE_DRIVER_URL = "http://selenium-release.storage.googleapis.com/2.45/IEDriverServer_Win32_2.45.0.zip"
    DOWNLOAD_DESTINATION_FOLDER_NAME = '.iedriver'

    @staticmethod
    def get_ie_driver():
        expected_file = os.path.join(IEDriverHelper._iedriver_folder(), 'IEDriverServer.exe')
        if not os.path.exists(expected_file):
            IEDriverHelper._download_zip()
            IEDriverHelper._extract_zip()

        return expected_file

    @staticmethod
    def _iedriver_folder():
        return DriverHelper.download_destination(IEDriverHelper.DOWNLOAD_DESTINATION_FOLDER_NAME)

    @staticmethod
    def _zip_location():
        dest = os.path.join(DriverHelper.download_destination(IEDriverHelper.DOWNLOAD_DESTINATION_FOLDER_NAME),
                            'download.zip')
        return dest

    @staticmethod
    def _download_zip():
        downloader = urllib.URLopener()
        downloader.retrieve(IEDriverHelper().IE_DRIVER_URL, IEDriverHelper._zip_location())

    @staticmethod
    def _extract_zip():
        if not os.path.exists(IEDriverHelper._zip_location()):
            raise Exception('IE Driver zip not in expected location')

        with zipfile.ZipFile(IEDriverHelper._zip_location(), 'r') as ie_driver_zip:
            ie_driver_zip.extractall(
                DriverHelper.download_destination(IEDriverHelper.DOWNLOAD_DESTINATION_FOLDER_NAME))

    @staticmethod
    def _download_ie_driver(destination_file):
        downloader = urllib.URLopener()
        downloader.retrieve(IEDriverHelper().IE_DRIVER_URL, destination_file)


class ChromeDriverHelper(object):
    DOWNLOAD_DESTINATION_FOLDER_NAME = '.chromedriver'

    @staticmethod
    def _latest_version():
        r = requests.get('http://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        return r.text.strip()

    @staticmethod
    def _download_url():
        url = "http://chromedriver.storage.googleapis.com/{0}/chromedriver_{1}32.zip".format(
            ChromeDriverHelper._latest_version(), DriverHelper.os_name())
        return url

    @staticmethod
    def _zip_location():
        dest = os.path.join(DriverHelper.download_destination(ChromeDriverHelper.DOWNLOAD_DESTINATION_FOLDER_NAME),
                            'download.zip')
        return dest

    @staticmethod
    def _download_chrome_driver_zip():
        downloader = urllib.URLopener()
        dest = ChromeDriverHelper._zip_location()
        downloader.retrieve(ChromeDriverHelper._download_url(), dest)

    @staticmethod
    def _extract_zip():
        if not os.path.exists(ChromeDriverHelper._zip_location()):
            raise Exception('Chromedriver zip not in expected location')

        with zipfile.ZipFile(ChromeDriverHelper._zip_location(), 'r') as chrome_zip:
            chrome_zip.extractall(
                DriverHelper.download_destination(ChromeDriverHelper.DOWNLOAD_DESTINATION_FOLDER_NAME))

    @staticmethod
    def _expected_file_name():
        if DriverHelper.os_name() is 'win':
            return 'chromedriver.exe'
        elif DriverHelper.os_name() is 'mac':
            return 'chromedriver'
        else:
            raise NotImplementedError()

    @staticmethod
    def get_chromedriver():
        expected_file = os.path.join(
            DriverHelper.download_destination(ChromeDriverHelper.DOWNLOAD_DESTINATION_FOLDER_NAME),
            ChromeDriverHelper._expected_file_name())
        if not os.path.exists(expected_file):
            ChromeDriverHelper._download_chrome_driver_zip()
            ChromeDriverHelper._extract_zip()
        return expected_file