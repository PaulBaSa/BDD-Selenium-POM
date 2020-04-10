import os
import platform

import dateparser
import pytest
from selenium import webdriver

from POM.pages.DeveloperGuidePage import DeveloperGuidePage
from bin.drivers import get_latest_drivers
from bin.drivers.get_latest_drivers import map_platform_gecko_os
from utils.SoftAssert import SoftAssert


@pytest.fixture()
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


class TestDatatable:

    def test_datatable(self, driver):
        # Soft assert, to verify without stopping the flow
        soft_assert = SoftAssert()

        input_data = {
            "row_to_edit": 3,
            "Label": "Larry Page",
            "Website": "https://google.com",
            "Phone number": "(555)-755-6575",
            "Date Time": dateparser.parse("Jan 01, 2022 12:57 PM"),
            "Balance": "770.54"

        }

        # STEP: Navigate to the link: https://developer.salesforce.com/docs/component-library/documentation/en/48.0/lwc
        driver.get("https://developer.salesforce.com/docs/component-library/documentation/en/48.0/lwc")
        developer_guide_page = DeveloperGuidePage(driver)

        # STEP: Switch to the Component Reference tab
        component_reference_page = developer_guide_page.nav_bar.go_to("component_reference")

        # STEP: Search in Quick Find for “datatable”
        component_reference_page.side_bar.quick_find = "datatable"

        # STEP: Under Lightning Web Components, click on the Components>lightning>“datatable” on the left menu panel
        component_reference_page.side_bar.click_on("datatable")

        # STEP: Under Example tab on the main pane > select “Datatable from Inline Edit” from the dropdown
        component_reference_page.datatable_component.example_combobox = "Data Table with Inline Edit"

        # STEP: Click on the “Open in Playground” button
        playground_page = component_reference_page.datatable_component.open_in_playground()

        # STEP: Under the rightmost section “Preview”
        #   Edit/Update the values for all the columns in row 3 in the table -
        #       Label: Larry Page
        #       Website: https://google.com
        #       Phone number:(555)-755-6575
        #       Date Time: Jan 01, 2022 12:57 PM
        #       Balance: 770.54
        preview_frame = playground_page.preview_frame
        with preview_frame.frame():
            table = preview_frame.table
            row_to_edit = input_data["row_to_edit"] - 1
            table[row_to_edit]["Label"] = input_data["Label"]
            table[row_to_edit]["Website"] = input_data["Website"]
            table[row_to_edit]["Phone"] = input_data["Phone number"]
            table[row_to_edit]["CloseAt"] = input_data["Date Time"]
            table[row_to_edit]["Balance"] = input_data["Balance"]

            #  STEP: Assert the above have been updated in the table
            new_values = {k: next(iter([e.text for e in v.find_elements_by_css_selector(".slds-truncate")]), "")
                          for k, v in table[row_to_edit].items()}
            # Prepare the expected values by:
            #   deleting row_to_edit as is not needed
            #   renaming "Phone Number" to Phone
            #   formatting the "Date Time" into the table format MMM d, YYYY adn renaming it to "CloseAt"
            #   and by adding the "$" sign at the beginning of the balance
            expected_values = input_data.copy()
            del expected_values["row_to_edit"]
            expected_values["Phone"] = expected_values.pop("Phone number")
            expected_values["CloseAt"] = expected_values.pop("Date Time").strftime("%b %-d, %Y")
            expected_values["Balance"] = f"{expected_values['Balance']}"

            for k, v in expected_values.items():
                # assert new_values[k] == v, f"Input values should match with the entered data for '{k}'"
                soft_assert.verify(new_values[k], v, f"Input values should match with the entered data for '{k}'")

        # STEP: Navigate back to the previous page
        #   and Repeat step 5 by selecting the “Datatable from Row Actions” from the dropdown
        driver.back()
        component_reference_page.datatable_component.example_combobox = "Data Table with Row Actions"

        # STEP: Click on the “Open in Playground” button
        playground_page = component_reference_page.datatable_component.open_in_playground()

        # STEP: Under the rightmost section “Preview” -> Scroll down to the end of the table
        preview_frame = playground_page.preview_frame
        with preview_frame.frame():
            # STEP: Click on the down caret icon for the last row and select “Show Details”
            table = preview_frame.table
            last_row = table[-1]
            name_on_table = table[-1]["Name"].text
            balance_on_table = table[-1]["Balance"].text
            last_row[""].click()
            driver.find_element_by_link_text("Show details").click()

            # STEP: Assert the record details “Name” and “Balance” are the same as
            #   the last row in the Blue Section below the table
            name_on_details = driver.find_element_by_xpath("//dt[text()='Name:']/following-sibling::dd").text
            # assert name_on_details == name_on_table, \
            #     "Name on table should match with name on record details"
            soft_assert.verify(name_on_details, name_on_table,
                               "Name on table should match with name on record details")

            balance_on_details = driver.find_element_by_xpath("//dt[text()='Balance:']/following-sibling::dd").text
            # assert balance_on_details == balance_on_table, \
            #     "Balance on table should match with balance on record details"
            soft_assert.verify(balance_on_details, balance_on_table,
                               "Balance on table should match with balance on record details")

        soft_assert.assert_all()
