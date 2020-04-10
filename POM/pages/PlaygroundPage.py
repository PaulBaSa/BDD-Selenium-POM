from datetime import datetime
from typing import List

from selenium import webdriver
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement

from POM.pages.BasePage import BasePage
from POM.pages.common.IFrame import IFrame


class PlaygroundPage(BasePage):

    def __init__(self, driver: webdriver):
        super().__init__(driver)
        self.wait_for_element_locator = {"by": By.XPATH, "value": ".//iframe"}
        self.preview_frame = self.PlaygroundFrame(self).preview_frame

    class PlaygroundFrame(IFrame):

        def __init__(self, parent):
            super().__init__(parent)
            self.preview_frame = self.PreviewFrame(self)

        class PreviewFrame(IFrame):

            def __init__(self, parent):
                super().__init__(parent)
                self.iframe_locator = {"by": By.NAME, "value": "preview"}
                self.wait_for_element_locator = {"by": By.XPATH, "value": ".//table/.//tr/td"}
                self.table_locator = {"by": By.TAG_NAME, "value": "table"}

                self.input_dialog_locator = {"by": By.XPATH, "value": "//section[@role='dialog']//input"}

            @property
            def input_dialog(self) -> webelement:
                return self.driver.find_element(**self.input_dialog_locator)

            @input_dialog.setter
            def input_dialog(self, value: str):
                self.input_dialog.clear()
                self.input_dialog.send_keys(value)
                self.input_dialog.submit()

            @property
            def input_date_dialog(self) -> List:
                return self.driver.find_elements(**self.input_dialog_locator)

            @input_date_dialog.setter
            def input_date_dialog(self, value):
                if isinstance(value, tuple) and len(value) == 2:
                    date = value[0]
                    time = value[1]

                    self.input_date_dialog[0].clear()
                    self.input_date_dialog[0].send_keys(date)

                    self.input_date_dialog[1].clear()
                    self.input_date_dialog[1].send_keys(time)
                    self.input_date_dialog[1].submit()

            @property
            def table(self) -> List:
                table = self.driver.find_element(**self.table_locator)
                all_rows = table.find_elements_by_xpath(".//tr")
                first_tr = all_rows[0].find_elements(By.XPATH, ".//th")

                headers = [th.get_attribute("innerText").split("\n")[0]
                           for th in
                           first_tr]  # if th.get_attribute("innerText") != ""]   # innerText cause text is hidden

                return [TableRow(dict(zip(headers, row.find_elements(By.CSS_SELECTOR, "th,td"))))
                        for row in all_rows[1:]]


class TableRow(dict):

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.driver = None

        for key, item in kwargs.items():
            self.__dict__[key] = item
            if self.driver is None or not isinstance(self.driver, WebDriver):
                self.driver = item.parent

        self.input_dialog_locator = {"by": By.XPATH, "value": "//section[@role='dialog']//input"}

    @property
    def input_dialog(self) -> webelement:
        return self.driver.find_element(**self.input_dialog_locator)

    @input_dialog.setter
    def input_dialog(self, value: str):
        self.input_dialog.clear()
        self.input_dialog.send_keys(value)
        self.input_dialog.submit()

    @property
    def input_date_dialog(self) -> List:
        return self.driver.find_elements(**self.input_dialog_locator)

    @input_date_dialog.setter
    def input_date_dialog(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            _date = value[0]
            _time = value[1]

            self.input_date_dialog[1].clear()
            self.input_date_dialog[1].send_keys(_time)
            self.input_date_dialog[0].clear()
            self.input_date_dialog[0].send_keys(_date)
            self.input_date_dialog[1].send_keys("")
            self.input_date_dialog[1].submit()

    def __setitem__(self, key, item):
        self.__dict__[key].find_element_by_css_selector("button").click()
        if isinstance(item, datetime):
            date = item.strftime("%b %-d, %Y")
            time = item.strftime("%H:%M %p")
            self.input_date_dialog = date, time
        else:
            self.input_dialog = item
