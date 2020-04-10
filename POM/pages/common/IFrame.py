from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class IFrame:
    def __init__(self, parent):
        self.parent = parent
        self.driver = parent.driver
        self.iframe_locator = {"by": By.TAG_NAME, "value": "iframe"}
        self.timeout = 10
        self.wait_for_element_locator = {"by": By.TAG_NAME, "value": "body"}

    @property
    def iframe(self) -> webelement:
        wait = WebDriverWait(self.driver, self.timeout)
        return wait.until(ec.visibility_of_element_located(self.iframe_locator.values()))

    def wait_for_frame(self):
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(ec.visibility_of_element_located(self.wait_for_element_locator.values()))

    @contextmanager
    def frame(self):
        if isinstance(self.parent, IFrame):
            with self.parent.frame():
                self.driver.switch_to.frame(self.iframe)
                self.wait_for_frame()
                yield
                self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(self.iframe)
            self.wait_for_frame()
            yield
            self.driver.switch_to.default_content()
