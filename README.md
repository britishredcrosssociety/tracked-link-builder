# Marketing tracked link builder

This tool creates links with query strings appended for:

- Google Analytics
- BRC's bespoke marketing campaign tracking systems (in use on donate.redcross.org.uk and with potential to be used on www.redcross.org.uk)

The tool is used to:

- ensure consistency of tracking across internal teams, given the high number of individuals that both plan marketing and have access to the reporting.
- ensure query strings are well-formed (e.g. special characters are removed)

Some links fall outside the capacity of this tool, which is just designed for the core business use cases. Links for non-standard ad hoc requests are created to fit the overall taxonomy and added to the [bespoke link log](https://github.com/britishredcrosssociety/tracked-link-builder/wiki/Bespoke-link-log) - paths with repeated use are then folded into the link builder.

## To add a new form element into the tracked link

1. add new form element, with a new ID
2. If you want to show/hide the new element:
    - wrap it in a div
    - get the ID for the element that determines when the div is shown/hidden, and make sure that 'rule element' is being noticed by the call rules for toggleFields()
    - reflect the new div ID in the show/hide rules within the actual toggleFields() function
3. Make sure that the case rules link up the new element ID with an existing tracked link element
    - Initialise the variable if necessary
4. [QA the report](https://docs.google.com/spreadsheets/d/1pzD-kL0I-uG1RDmMqatHPOaYJfPGoVP5YEzHmm4lAZ0/edit#gid=1682837906)

## Automated testing

The `automated_checks.py` script automates the different test scenarios, and programmatically generates a list of links for the [link builder QA](https://docs.google.com/spreadsheets/d/1pzD-kL0I-uG1RDmMqatHPOaYJfPGoVP5YEzHmm4lAZ0/edit?gid=1682837906#gid=1682837906) sheet.

#### ChromeDriver

The script will fail if the version of ChromeDriver doesn't match the computer's version of Chrome. As on BRC laptops, the org manages the Chrome updates, this can happen regularly.

Trying to automate fixing this (using e.g. `ChromeDriverManager().install()`) just caused different problems (i.e. a `WebDriverException` error from the auto-DLed exe being in a folder where I don't have run permissions).

=> if the version clash error occurs:

1. ensure that Chrome is up to date (may require a close and open)
2. Go to https://googlechromelabs.github.io/chrome-for-testing/
3. Download the latest "chromedriver win64" version, and unzip it.
4. Point the `cService` variable to the (now correct version of) ChromeDriver.
