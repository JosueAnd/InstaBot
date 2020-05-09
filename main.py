import selenium.common.exceptions
from selenium import webdriver
from time import sleep


class InstaBot:
    def __init__(self, username, password):
        """ Get an instance of a web browser and login to Instagram. """

        # InstaBot instance variables.
        self.driver = webdriver.Firefox()   # Firefox web browser.
        self.username = username            # Instagram username.
        self.password = password            # Instagram password.

        # Opening Instagram page, logging in and enabling pop-ups.
        self._open_instagram()
        self._login()
        self._enable_pop_ups()

    def _enable_pop_ups(self):
        """ Look for the enable notifications pop-up. Respond with enable. """
        try:
            notifications = self.driver.find_element_by_xpath(
                '//div[@role="dialog"]')
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            notifications.find_element_by_xpath(
                '//button[contains(text(), "Turn On")]').click()

    def _login(self):
        """
            Type the username and password into their respective fields and
            click the submit button.
        """
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)

        # Find and click the submit button.
        submit_button = self.driver.find_element_by_xpath(
            '//button[@type="submit"]')
        submit_button.click()

        # Wait for the page to load.
        sleep(5)

    def _open_instagram(self):
        """ Navigate to Instagram and wait for the page to load. """
        self.driver.get("https://instagram.com")
        sleep(3)


InstaBot(username=4079029897, password='Josue1234!')
