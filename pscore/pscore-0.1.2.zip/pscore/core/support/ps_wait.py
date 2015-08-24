from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class PSWait(object):
    def __init__(self, driver):
        self.driver = driver

    def _wait_until_visible(self, locator, timeout, message, is_visible):
        if message is None:
            message = "Could not find {} in {} seconds".format(str(locator), timeout)

        wait = WebDriverWait(self.driver, timeout)
        if is_visible:
            wait.until(EC.visibility_of_element_located(locator), message=message)
        else:
            wait.until(EC.invisibility_of_element_located(locator), message=message)

    def until_visible(self, locator, timeout=3, message=None):
        self._wait_until_visible(locator, timeout, message, True)

    def until_not_visible(self, locator, timeout=3, message=None):
        self._wait_until_visible(locator, timeout, message, False)



