import datetime
from os.path import abspath
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pytimeparse.timeparse import timeparse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
    element_to_be_clickable as clickable, \
    presence_of_element_located as present, \
    presence_of_all_elements_located as all_present, \
    staleness_of as stale, \
    visibility_of as visible, \
    text_to_be_present_in_element_value as elem_value

from locators import RecordingsLocators, \
                                             UploadLocators, \
                                             TrimLocators, \
                                             LoginLocators, \
                                             AdminLocators

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def reload(self):
        self.driver.refresh()

    def default_frame(self):
        self.driver.switch_to.default_content()

    def js(self, *args):
        self.driver.execute_script(*args)

    def switch_frame(self, frame_elem):
        self.driver.switch_to.frame(frame_elem)

    def get_element(self, locator, condition=clickable):
        if condition is not None:
            return WebDriverWait(self.driver, 10).until(condition(locator))
        else:
            return self.driver.find_element(*locator)

    def get_elements(self, locator, condition=all_present):
        if condition is not None:
            return WebDriverWait(self.driver, 10).until(condition(locator))
        else:
            return self.driver.find_elements(*locator)

    def set_checkbox(self, cb, enabled):
        if enabled and not cb.is_selected():
            cb.click()
        elif not enabled and cb.is_selected():
            cb.click()

    def enter_text(self, elem, text):
        elem.send_keys(text)
        return WebDriverWait(self.driver, 10).until(
            lambda x: elem.get_attribute('value') == text
        )

class LoginPage(BasePage):

    @property
    def username_input(self):
        return self.get_element(LoginLocators.USERNAME_INPUT)

    @property
    def password_input(self):
        return self.get_element(LoginLocators.PASSWORD_INPUT)

    @property
    def submit(self):
        return self.get_element(LoginLocators.SUBMIT_BUTTON)

    def login(self, username, password):
        self.username_input.send_keys(username)
        self.password_input.send_keys(password)
        self.submit.click()

class AdminPage(BasePage):

    @property
    def recordings_tab(self):
        return self.get_element(AdminLocators.RECORDINGS_TAB)

class RecordingsPage(AdminPage):

    @property
    def upload_recording_button(self):
        return self.get_element(RecordingsLocators.UPLOAD_RECORDING_BUTTON)

    @property
    def search_select(self):
        return Select(self.get_element(RecordingsLocators.SEARCH_SELECT, clickable))

    @property
    def search_input(self):
        return self.get_element(RecordingsLocators.SEARCH_INPUT, clickable)

    @property
    def per_page_select(self):
        return Select(self.get_element(RecordingsLocators.PERPAGE_SELECT, clickable))

    @property
    def refresh_checkbox(self):
        return self.get_element(RecordingsLocators.REFRESH_CHECKBOX, clickable)

    @property
    def on_hold_tab(self):
        return self.get_element(RecordingsLocators.ON_HOLD_TAB, clickable)


    @property
    def trim_iframe(self):
        return self.get_element(RecordingsLocators.TRIM_IFRAME)

    @property
    def trim_links(self):
        return self.get_elements(RecordingsLocators.TRIM_LINK)

    def refresh_off(self):
        self.set_checkbox(self.refresh_checkbox, False)
        self.js('window.clearInterval(ocRecordings.refreshInterval);')

    def filter_recordings(self, field, value):
        self.search_select.select_by_value(field)
        self.search_input.send_keys(value)
        self.search_input.send_keys(Keys.RETURN)
        found = self.get_element(RecordingsLocators.FILTER_FOUND_COUNT, present)
        return found

    def max_per_page(self):
        self.per_page_select.select_by_visible_text('100')

    def switch_to_tab(self, tab_elem):
        """
        bypass the usual element click() method as these tab links frequently
        throw exceptions about not being clickable at point blah, blah
        """
        self.driver.execute_script("arguments[0].click();", tab_elem)

class UploadPage(BasePage):

    @property
    def title_input(self):
        return self.get_element(UploadLocators.TITLE_INPUT)

    @property
    def presenter_input(self):
        return self.get_element(UploadLocators.PRESENTER_INPUT)

    @property
    def course_input(self):
        return self.get_element(UploadLocators.COURSE_INPUT)

    @property
    def license_select(self):
        return Select(self.get_element(UploadLocators.LICENSE_SELECT))

    @property
    def rec_date_input(self):
        return self.get_element(UploadLocators.REC_DATE_INPUT)

    @property
    def start_hour_select(self):
        return Select(self.get_element(UploadLocators.START_HOUR_SELECT))

    @property
    def start_minute_select(self):
        return Select(self.get_element(UploadLocators.START_MINUTE_SELECT))

    @property
    def contributor_input(self):
        return self.get_element(UploadLocators.CONTRIBUTOR_INPUT)

    @property
    def type_input(self):
        return self.get_element(UploadLocators.TYPE_INPUT)

    @property
    def subject_input(self):
        return self.get_element(UploadLocators.SUBJECT_INPUT)

    @property
    def lang_input(self):
        return self.get_element(UploadLocators.LANG_INPUT)

    @property
    def desc_input(self):
        return self.get_element(UploadLocators.DESC_INPUT)

    @property
    def copyright_input(self):
        return self.get_element(UploadLocators.COPYRIGHT_INPUT)

    @property
    def single_file_radio(self):
        return self.get_element(UploadLocators.SINGLE_FILE_RADIO)

    @property
    def multi_file_radio(self):
        return self.get_element(UploadLocators.MULTI_FILE_RADIO)

    @property
    def single_file_local_radio(self):
        return self.get_element(UploadLocators.SINGLE_FILE_LOCAL_RADIO)

    @property
    def single_file_inbox_radio(self):
        return self.get_element(UploadLocators.SINGLE_FILE_INBOX_RADIO)

    @property
    def multi_file_presentation_local_radio(self):
        return self.get_element(UploadLocators.MULTI_FILE_PRESENTATION_LOCAL_RADIO)

    @property
    def multi_file_presenter_local_radio(self):
        return self.get_element(UploadLocators.MULTI_FILE_PRESENTER_LOCAL_RADIO)

    @property
    def multi_file_presentation_inbox_radio(self):
        return self.get_element(UploadLocators.MULTI_FILE_PRESENTATION_INBOX_RADIO)

    @property
    def multi_file_presenter_inbox_radio(self):
        return self.get_element(UploadLocators.MULTI_FILE_PRESENTER_INBOX_RADIO)

    @property
    def file_input_iframes(self):
        return self.get_elements(UploadLocators.FILE_INPUT_IFRAME)

    @property
    def local_file_selector(self):
        return self.get_element(UploadLocators.LOCAL_FILE_SELECTOR)

    @property
    def inbox_file_select(self):
        return Select(self.get_element(UploadLocators.INBOX_FILE_SELECT))

    @property
    def contains_slides_checkbox(self):
        return self.get_element(UploadLocators.CONTAINS_SLIDES_CHECKBOX)

    @property
    def workflow_select(self):
        return Select(self.get_element(UploadLocators.WORKFLOW_SELECT))

    @property
    def live_stream_checkbox(self):
        return self.get_element(UploadLocators.LIVE_STREAM_CHECKBOX)

    @property
    def multitrack_checkbox(self):
        return self.get_element(UploadLocators.MULTITRACK_CHECKBOX)

    @property
    def upload_button(self):
        return self.get_element(UploadLocators.UPLOAD_BUTTON)

    @property
    def upload_progress_dialog(self):
        return self.get_element(UploadLocators.UPLOAD_PROGRESS_DIALOG)

    def set_live_stream(self, enabled):
        self.set_checkbox(self.live_stream_checkbox, enabled)

    def set_multitrack(self, enabled):
        self.set_checkbox(self.multitrack_checkbox, enabled)

    def set_upload_files(self, presenter=None, presentation=None, combined=None,
                         is_inbox=False):
        """
        The MH upload UI does some crazy stuff with iframes.
        None of the iframe elements have unique ids, so this
        and the subsequent _private methods have to make some
        assumptions about the order in which they are returned
        by the locator elements.
        """
        if combined is not None:
            self.single_file_radio.click()
            if is_inbox:
                self.single_file_inbox_radio.click()
            else:
                self.single_file_local_radio.click()
            self.set_upload_file(self.file_input_iframes[0], combined, is_inbox)
        else:
            self.multi_file_radio.click()
            if is_inbox:
                self.multi_file_presentation_inbox_radio.click()
                self.multi_file_presenter_inbox_radio.click()
            else:
                self.multi_file_presentation_local_radio.click()
                self.multi_file_presenter_local_radio.click()
            self.set_upload_file(self.file_input_iframes[1], presentation, is_inbox)
            self.set_upload_file(self.file_input_iframes[2], presenter, is_inbox)

    def set_upload_file(self, iframe, file, is_inbox):
        self.driver.switch_to.frame(iframe)
        if is_inbox:
            self.inbox_file_select.select_by_value(file)
        else:
            # NOTE: this will silently fail if it's not an absolute path to an existing file
            self.local_file_selector.send_keys(abspath(file))
        self.driver.switch_to.default_content()

    def wait_for_upload_finish(self):
        WebDriverWait(self.driver, 1000000).until_not(visible(self.upload_progress_dialog))

class TrimPage(BasePage):

    @property
    def shortcut_table(self):
        return self.get_element(TrimLocators.SHORTCUT_TABLE)

    @property
    def trim_begin_input(self):
        return self.get_element(TrimLocators.CLIP_BEGIN_INPUT)

    @property
    def trim_end_input(self):
        return self.get_element(TrimLocators.CLIP_END_INPUT)

    @property
    def trim_ok_button(self):
        return self.get_element(TrimLocators.CLIP_OK_BUTTON)

    @property
    def split_remover(self):
        return self.get_element(TrimLocators.CLIP_REMOVE_BUTTON)

    @property
    def continue_button(self):
        return self.get_element(TrimLocators.CONTINUE_BUTTON)

    @property
    def clear_button(self):
        return self.get_element(TrimLocators.CLEAR_BUTTON)

    def trim(self):
        self.clear_button.click()
        sleep(1)
        # safe to assume media is > 10 seconds?
        self.shortcut_table.send_keys("l" * 20)
        sleep(1)
        self.shortcut_table.send_keys("v")
        sleep(1)
        self.shortcut_table.send_keys(Keys.ARROW_UP)
        sleep(1)
        self.shortcut_table.send_keys(Keys.DELETE)
        sleep(1)

        # media_length = timeparse(self.trim_end_input.get_attribute('value'))
        # trim_length = media_length / 10
        # self.trim_begin_input.clear()
        # self.trim_begin_input.send_keys(str(datetime.timedelta(seconds=trim_length)))
        # self.trim_ok_button.click()
        # sleep(2)
        # self.split_remover.click()

        self.continue_button.click()
        sleep(2)
