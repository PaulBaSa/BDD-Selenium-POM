from selenium import webdriver

from POM.pages.BasePage import BasePage


class DeveloperGuidePage(BasePage):

    def __init__(self, driver: webdriver):
        super().__init__(driver)
