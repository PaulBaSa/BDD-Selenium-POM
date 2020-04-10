from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from POM.pages.PlaygroundPage import PlaygroundPage


class Component:

    def __init__(self, parent):
        self.parent = parent
        self.driver = self.parent.driver
        self.element_locator = {"by": By.ID, "value": "skip-target-content"}
        self.timeout = 10
        self.example_combobox_locator = {"by": By.XPATH,
                                         "value": ".//lightning-combobox/label[text()='Example']/.."}
        self.open_playground_locator = {"by": By.XPATH, "value": ".//button[text()='Open in Playground']"}

        self.wait_for_element_locator = {"by": By.NAME, "value": "preview"}

    @property
    def element(self) -> webelement:
        self.wait_for_component()
        return self.driver.find_element(**self.element_locator)

    def wait_for_component(self):
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(ec.visibility_of_element_located(self.wait_for_element_locator.values()))

    @property
    def example_combobox(self):
        return self.element.find_element(**self.example_combobox_locator)

    @example_combobox.setter
    def example_combobox(self, value):
        if value is not None:
            self.example_combobox.find_element_by_tag_name("input").click()
            listbox = self.example_combobox.find_element_by_xpath(".//div[@role='listbox']")
            available_options = listbox.find_elements_by_xpath(".//span[@class='slds-truncate']")
            option = list(filter(lambda op: op.text == value, available_options))
            if len(option):
                option[0].click()
            else:
                str_available_options = "\n\t\t".join([op.text for op in available_options])
                err_msg = f"Unavailable option '{value}' under combobox.\n\t" \
                          f"Available options are: \n\t\t{str_available_options}"
                print(err_msg)
                raise Exception(err_msg)

    @property
    def btn_open_in_playground(self):
        return self.element.find_element(**self.open_playground_locator)

    def open_in_playground(self) -> PlaygroundPage:
        self.btn_open_in_playground.click()
        page = PlaygroundPage(self.driver)
        page.wait_for_page()
        return page
