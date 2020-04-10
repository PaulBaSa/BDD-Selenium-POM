#Navigate to the link: https://developer.salesforce.com/docs/component-library/documentation/en/48.0/lwc
#Switch to the Component Reference tab
#Search in Quick Find for “datatable”
#Under Lightning Web Components, click on the Components>lightning>“datatable” on the left menu panel
#Under Example tab on the main pane > select “Datatable from Inline Edit” from the dropdown
#Click on the “Open in Playground” button
#Under the rightmost section “Preview” -> Edit/Update the values for all the columns in row 3 in the table -
#Label: Larry Page
#Website: https://google.com
#Phone number:(555)-755-6575
#Date Time: Jan 01, 2022 12:57 PM
#Balance: 770.54
#Assert the above have been updated in the table
#Navigate back to the previous page and Repeat step 5 by selecting the “Datatable from Row Actions” from the dropdown
#Click on the “Open in Playground” button
#Under the rightmost section “Preview” -> Scroll down to the end of the table
#Click on the down caret icon for the last row and select “Show Details”
#Assert the record details “Name” and “Balance” are the same as the last row in the Blue Section below the table

Feature: Test Datatable component
  As a web user,
  I want to be able to edit rows when using datatable component
  with "Datatable from Inline Edit" example

#  Background:
#    Given the Introducing Lightning Web Components home page is displayed

  Scenario: Datatable from Inline Edit
    Given the Introducing Lightning Web Components home page is displayed
    When the user Switch to the Component Reference tab
    And Search in Quick Find for "datatable"
    And click on the Components>lightning>"datatable"
    And select "Data Table with Inline Edit" from the Example dropdown
    And click on the "Open in Playground" button
    And Under "Preview" section edit the values for all the columns in row 3 in the table
      """
       Label: Larry Page
       Website: https://google.com
       Phone number: (555)-755-6575
       Date Time: Jan 01, 2022 12:57 PM
       Balance: 770.54
      """
    Then validate entered data in row 3 have been updated in the table.

  Scenario: Data Table with Row Actions
    When  Navigate back to the previous page
    And  select "Data Table with Row Actions" from the Example dropdown
    And  click on the "Open in Playground" button
    And  Under "Preview" section Scroll down to the end of the table
    And  Click on the down caret icon for the last row and select "Show details"
    Then Validate record details "Name" and "Balance" are the same as the last row in the Blue Section


