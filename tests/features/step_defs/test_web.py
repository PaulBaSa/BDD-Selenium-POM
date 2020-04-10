"""
This module contains step definitions for web.feature.
It uses Selenium WebDriver for browser interactions:
https://www.seleniumhq.org/projects/webdriver/
Setup and cleanup are handled using hooks.
For a real test automation project,
use Page Object Model or Screenplay Pattern to model web interactions.
"""
import os
import platform
from functools import partial

import dateparser
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver

from POM.pages.DeveloperGuidePage import DeveloperGuidePage
from bin.drivers import get_latest_drivers
from bin.drivers.get_latest_drivers import map_platform_gecko_os
from utils.Common import to_row_index
# Constants
from utils.SoftAssert import SoftAssert

BASE_URL = 'https://developer.salesforce.com/docs/component-library/documentation/en/48.0/lwc'

CONVERTERS = {
    'row_index': to_row_index,
}

# Scenarios

when = partial(when, converters=CONVERTERS)
then = partial(then, converters=CONVERTERS)

scenarios('../web.feature', )  # strict_gherkin=False)


# Context Class

class Context:
    def __init__(self, driver):
        self.driver = driver


# Fixtures
@pytest.fixture(scope="package")
def driver():
    """
    Fixture used to setup and teardown on each function (default scope)
    :return: None
    """

    current_platform = f"{platform.system()} {platform.machine()}"
    current_gecko_os = map_platform_gecko_os.get(current_platform, current_platform)
    drivers_path = os.path.dirname(get_latest_drivers.__file__)
    gecko_path = f"{drivers_path}/{current_gecko_os}/geckodriver"

    driver = webdriver.Firefox(executable_path=gecko_path)
    driver.implicitly_wait(1)
    driver.maximize_window()

    yield driver

    driver.close()


@pytest.fixture(scope="package")
def context(driver):
    return Context(driver)


# Given Steps

@given('the Introducing Lightning Web Components home page is displayed')
def lwc_home(context):
    context.driver.get(BASE_URL)
    context.developer_guide_page = DeveloperGuidePage(context.driver)
    context.soft_assert = SoftAssert()


# When Steps

@when(parsers.parse('the user Switch to the {tab} tab'))
def switch_to_tab(context, tab):
    context.component_reference_page = context.developer_guide_page.nav_bar.go_to(tab)


@when(parsers.parse('Search in Quick Find for "{component}"'))
def search_in_quick_find(context, component):
    context.component_reference_page.side_bar.quick_find = component


@when(parsers.parse('click on the Components>lightning>"{component}"'))
def side_bar_click_on(context, component):
    context.component_reference_page.side_bar.click_on(component)


@when(parsers.parse('select "{dropdown_option}" from the Example dropdown'))
def side_bar_click_on(context, dropdown_option):
    context.component_reference_page.datatable_component.example_combobox = dropdown_option


@when(parsers.parse('click on the "Open in Playground" button'))
def click_on(context, ):
    # STEP: Click on the "Open in Playground" button
    context.playground_page = context.component_reference_page.datatable_component.open_in_playground()


@when(parsers.parse('Under "Preview" section edit the values for all the columns in row {row_to_edit:d} in the table\n'
                    '"""{fields}"""'))
def edit_row_data(context, row_to_edit, fields):
    # STEP: Under the rightmost section "Preview"
    #   Edit/Update the values for all the columns in row 3 in the table -
    #       Label: Larry Page
    #       Website: https://google.com
    #       Phone number:(555)-755-6575
    #       Date Time: Jan 01, 2022 12:57 PM
    #       Balance: 770.54
    _row_to_edit = row_to_edit - 1
    context.input_data = {f.split(': ')[0].strip(): f.split(': ')[1].strip() for f in fields.split('\n') if len(f)}
    preview_frame = context.playground_page.preview_frame
    with preview_frame.frame():
        table = preview_frame.table
        table[_row_to_edit]["Label"] = context.input_data["Label"]
        table[_row_to_edit]["Website"] = context.input_data["Website"]
        table[_row_to_edit]["Phone"] = context.input_data["Phone number"]
        table[_row_to_edit]["CloseAt"] = dateparser.parse(context.input_data["Date Time"])
        table[_row_to_edit]["Balance"] = context.input_data["Balance"]


@when(parsers.parse('Navigate back to the previous page'))
def navigate_back(context):
    # STEP: Navigate back to the previous page
    context.driver.back()


@when(parsers.parse('Under "Preview" section Scroll down to the {row_index} of the table'))
def scroll_down_to_element(context, row_index):
    # STEP: Under the rightmost section "Preview" -> Scroll down to the end of the table
    preview_frame = context.playground_page.preview_frame
    with preview_frame.frame():
        # STEP: Click on the down caret icon for the last row and select "Show Details"
        table = preview_frame.table
        last_row = table[row_index]
        element = list(last_row.values())[0]
        element.click()
        # ActionChains(context.driver).move_to_element(element).perform()
        # context.driver.execute_script("arguments[0].scrollIntoView();", element)


@when(parsers.parse('Click on the down caret icon for the {row_index} row and select "{option}"'))
def click_on_down_caret_and_select(context, row_index, option):
    preview_frame = context.playground_page.preview_frame
    with preview_frame.frame():
        # STEP: Click on the down caret icon for the last row and select "Show Details"
        table = preview_frame.table
        last_row = table[row_index]
        last_row[""].click()
        context.driver.find_element_by_link_text(option).click()


# Then Steps

@then(parsers.parse('validate entered data in row {row_to_validate:d} have been updated in the table.'))
def validate_table(context, row_to_validate):
    #  STEP: Assert the above have been updated in the table
    preview_frame = context.playground_page.preview_frame
    with preview_frame.frame():
        table = preview_frame.table

        new_values = {k: next(iter([e.text for e in v.find_elements_by_css_selector(".slds-truncate")]), "")
                      for k, v in table[row_to_validate - 1].items()}

    # Prepare the expected values by:
    #   renaming "Phone Number" to Phone
    #   formatting the "Date Time" into the table format MMM d, YYYY adn renaming it to "CloseAt"
    #   and by adding the "$" sign at the beginning of the balance
    expected_values = context.input_data.copy()
    expected_values["Phone"] = expected_values.pop("Phone number")
    expected_values["CloseAt"] = dateparser.parse(expected_values.pop("Date Time")).strftime("%b %-d, %Y")
    expected_values["Balance"] = f"{expected_values['Balance']}"

    for k, v in expected_values.items():
        context.soft_assert.verify(new_values[k], v,
                                   f"Input values should match with the entered data for '{k}'")

    context.soft_assert.assert_all()


@then(parsers.parse('Validate record details {fields} are the same as the {row_index} row in the Blue Section'))
def validate_datatable_vs_blue_section(context, fields, row_index):
    _fields = fields.lower().replace('"', '').replace(',', '').replace(' and ', ' ').split(" ")
    map_table_blue = {'name': 'Name:', 'balance': "Balance:"}
    preview_frame = context.playground_page.preview_frame
    with preview_frame.frame():
        table = preview_frame.table
        # STEP: Assert the record details "Name" and "Balance" are the same as
        #   the last row in the Blue Section below the table
        for f in _fields:
            f = f.strip()
            in_blue = map_table_blue.get(f)
            on_table = table[row_index][f.title()].text
            on_details = context.driver.find_element_by_xpath(f"//dt[text()='{in_blue}']/following-sibling::dd").text
            assert on_details == on_table, f"{f.title()} on table should match with {in_blue} on record details"
