from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils.Common import snake_case


class BasePage:

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.nav_bar = self.NavBar(self)

        self.timeout = 5
        self.wait_for_element_locator = {"by": By.LINK_TEXT, "value": "Component Reference"}

    def wait_for_page(self):
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(ec.visibility_of_element_located(self.wait_for_element_locator.values()))

    class NavBar:

        def __init__(self, parent):
            self.parent = parent
            self.driver = self.parent.driver

            # Menus
            # Component Reference
            self.component_reference_tab_locator = {"by": By.LINK_TEXT, "value": "Component Reference"}

        @property
        def component_reference_tab(self):
            return self.driver.find_element(**self.component_reference_tab_locator)

        def go_to(self, place: str):
            place = snake_case(place)
            existing_tabs_menus = {
                "component_reference": self.component_reference_tab,
            }
            if place not in existing_tabs_menus.keys():
                print(f"The provided place to go \"{place}\" is not implemented yet, please code it!.")
                str_existing_places = "\n\t".join(existing_tabs_menus.keys())
                print(f"Existing places : \n\t{str_existing_places}")
                raise NotImplementedError

            page_to_go = None
            if place == "component_reference":
                from POM.pages.ComponentReferencePage import ComponentReferencePage
                page_to_go = ComponentReferencePage(self.driver)

            existing_tabs_menus[place].click()
            page_to_go.wait_for_page()
            return page_to_go
