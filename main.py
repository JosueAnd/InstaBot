from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep

from exceptions import *


class InstaBot:
    def __init__(self, username, password):
        """
            Get an instance of a web browser, login to Instagram and start auto-liking.\n

            :arg
                -   username:   Phone number, email, whatever you use to login to Instagram.
                -   password:   Your Instagram password associated with the username.
        """

        # InstaBot instance variables.
        self.driver = webdriver.Firefox()  # Firefox web browser.
        self.wait = WebDriverWait(self.driver, 10)  # Wait functionality.
        self.username = username  # Instagram username.
        self.password = password  # Instagram password.

        # Opening Instagram page, logging in and enabling pop-ups.
        if self._open_instagram():
            if self._login():
                self._disable_notifications()
                self.run()

    def run(self):
        """
            Run the script indefinitely.
        """
        while True:
            if self._find_user('creativesoulmedia'):
                self._like_posts()
                # Sleep for one hour before checking again.
                sleep(60 * 60)

    def _disable_notifications(self):
        """
            Look for the enable notifications pop-up. Respond with disable.
        """
        if self._wait_until(e_c.presence_of_element_located, By.XPATH, '//div[@role="dialog"]'):
            notifications = self.driver.find_element(By.XPATH, '//div[@role="dialog"]')
            # If the pop-up is found, click Not Now to notifications.
            notifications.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()

    def _find_user(self, user):
        """
            Find a user and navigate to their page.\n

            :arg
                -   user:   A string of the username of the user you intend to find.
            :returns
                -   True on success of _login() attempt.
            :raises
                -   UserNotFoundError
        """
        if self._wait_until(e_c.presence_of_element_located, By.CSS_SELECTOR,
                            'input[placeholder="Search"') is not None:
            search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search"')
            search_bar.send_keys(str(user))
            if self._wait_until(e_c.presence_of_element_located,
                                By.CSS_SELECTOR, 'a[href="/' + str(user) + '/"]'):
                user_found = self.driver.find_element(
                    By.CSS_SELECTOR, 'a[href="/' + str(user) + '/"]'
                )
                user_found.click()
                return True
            else:
                raise UserNotFoundError

    def _like_posts(self):
        if self._wait_until(e_c.presence_of_all_elements_located, By.CSS_SELECTOR, 'article a'):
            posts = self.driver.find_elements(By.CSS_SELECTOR, 'article a')
            for post in posts:
                self._wait_until(e_c.presence_of_element_located, By.CSS_SELECTOR,
                                     'button svg[aria-label*="like"]')
                try:
                    like_button = post.find_element(By.CSS_SELECTOR,
                                                    'button svg[aria-label*="like"]')
                except NoSuchElementException:
                    pass
                else:
                    if 'Like' in like_button.get_attribute('aria-label'):
                        like_button.click()
                    close_button = self.driver.find_element(By.CSS_SELECTOR,
                                            'button svg[aria-label="Close"]')
                    close_button.click()

    def _login(self):
        """
            Type the username and password into their respective fields and click the submit
            button.\n

            :returns
                -   True on success of _login() attempt.
            :raises
                -   LoginError
        """
        if self._wait_until(e_c.presence_of_element_located, By.NAME, 'username'):
            # Send username to Username field.
            username_field = self.driver.find_element(By.NAME, 'username')
            username_field.clear()
            username_field.send_keys(self.username)
            # Send password to Password field.
            password_field = self.driver.find_element(By.NAME, 'password')
            password_field.clear()
            password_field.send_keys(self.password)
            # Find and click the submit button.
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            return True
        else:
            raise LoginError

    def _open_instagram(self):
        """
            Navigate to Instagram and wait for the page to load.\n

            :returns
                -   True on success of self.driver.get('https://instagram.com').
            :raises
                -   selenium.common.exceptions.WebDriverException
        """
        try:
            self.driver.get('https://instagram.com')
        except WebDriverException:
            raise
        else:
            return True

    def _wait_until(self, condition, search_method, search_specifier):
        """
            Abstracting the exception logic of WebDriverWait.until (TimeoutException) into its own
            method.\n

            :arg
                -   condition:          A condition specified in
                                        selenium.webdriver.support.expected_conditions
                -   search_method:      A By._ locator strategy from selenium.webdriver.common.by
                -   search_specifier:    String search value as it relates to the search_method
            :returns
                -   Boolean value representing success or failure of self.wait.until(...).
        """
        try:
            self.wait.until(condition((search_method, search_specifier)))
        except TimeoutException:
            # Notify of timeout
            return False
        else:
            return True


insta_bot = InstaBot(username=4079029897, password='na!')
