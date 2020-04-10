from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement

from POM.pages.BasePage import BasePage
from POM.pages.common.Component import Component


class ComponentReferencePage(BasePage):

    def __init__(self, driver: webdriver):
        super().__init__(driver)

        self.side_bar = self.SideBar(self)
        self.datatable_component = self.Datatable(self)

        self.wait_for_element_locator = {"by": By.NAME, "value": "Quick Find"}

    class SideBar:

        def __init__(self, parent):
            self.parent = parent
            self.driver = self.parent.driver
            self.element_locator = {"by": By.TAG_NAME, "value": "componentreference-sidebar"}
            self.quick_find_locator = {"by": By.NAME, "value": "Quick Find"}

        @property
        def element(self) -> webelement:
            return self.driver.find_element(**self.element_locator)

        @property
        def quick_find(self) -> webelement:
            return self.driver.find_element(**self.quick_find_locator)

        @quick_find.setter
        def quick_find(self, value: str):
            self.quick_find.clear()
            self.quick_find.send_keys(value)

        def click_on(self, link_text):
            available_links = self.element.find_elements(By.XPATH, f".//span[contains(text(), '{link_text}')]")
            assert len(available_links), "There should be at least 1 link to click on"
            available_links[0].click()

    class Datatable(Component):

        def __init__(self, parent):
            super().__init__(parent)
