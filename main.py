from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep


class InstaBot:
    def __init__(self, username, password):
        """ Get an instance of a web browser and login to Instagram. """

        # InstaBot instance variables.
        self.driver = webdriver.Firefox()  # Firefox web browser.
        self.wait = WebDriverWait(self.driver, 10)  # Wait functionality.
        self.username = username  # Instagram username.
        self.password = password  # Instagram password.

        # Opening Instagram page, logging in and enabling pop-ups.
        self._open_instagram()
        self._login()
        self._enable_pop_ups()
        self.run()

    def run(self):
        """ Run the script indefinitely. """
        while True:
            self._find_user('creativesoulmedia')
            self._like_posts()
            # Sleep for one hour before checking again.
            sleep(60*60)

    def _enable_pop_ups(self):
        """ Look for the enable notifications pop-up. Respond with enable. """
        try:
            # Wait a max of 5 seconds until the pop-up is loaded onto the page.
            self.wait.until(e_c.presence_of_element_located(
                    (By.XPATH, '//div[@role="dialog"]')
            ))
        except TimeoutException:
            # If the pop-up is not found, end method procedures.
            pass
        else:
            notifications = self.driver.find_element(By.XPATH,
                                                     '//div[@role="dialog"]')
            # If the pop-up is found, click Turn On notifications.
            notifications.find_element_by_xpath(
                '//button[contains(text(), "Turn On")]').click()

    def _find_user(self, user):
        """ Find a user and navigate to their page. """
        try:
            # Wait a max of 5 seconds until the search bar is loaded onto the
            # page.
            self.wait.until(e_c.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[placeholder="Search"')
            ))
        except TimeoutException:
            pass
        else:
            search_bar = self.driver.find_element(By.CSS_SELECTOR,
                                                  'input[placeholder="Search"')
            search_bar.send_keys(str(user))
            try:
                self.wait.until(e_c.presence_of_element_located(
                    (By.CSS_SELECTOR, 'a[href="/' + str(user) + '/"]')
                ))
            except TimeoutException:
                pass
            else:
                user_found = self.driver.find_element(
                    By.CSS_SELECTOR, 'a[href="/' + str(user) + '/"]'
                )
                user_found.click()

    def _like_posts(self):
        try:
            self.wait.until(e_c.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'article>div')
            ))
        except TimeoutException:
            pass
        else:
            posts = self.driver.find_elements(By.CSS_SELECTOR, 'article>img')
            for post in posts:
                print(post.text)
                # try:
                #     self.wait.until(e_c.presence_of_element_located(
                #         (By.CSS_SELECTOR, 'button svg[aria-label*="like"]')
                #     ))
                #     like_button = self.driver.find_element(By.CSS_SELECTOR,
                #                                'button svg[aria-label*="like"]')
                # except NoSuchElementException:
                #     pass
                # else:
                #     if 'Like' in like_button.get_attribute('aria-label'):
                #         like_button.click()
                #     close_button = self.driver.find_element(By.CSS_SELECTOR,
                #                             'button svg[aria-label="Close"]')
                #     close_button.click()

    def _login(self):
        """
            Type the username and password into their respective fields and
            click the submit button.
        """
        try:
            self.wait.until(e_c.presence_of_element_located((By.NAME,
                                                             'username')))
        except TimeoutException:
            pass
        else:
            self.driver.find_element(By.NAME, 'username').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password)

            # Find and click the submit button.
            submit_button = self.driver.find_element(By.CSS_SELECTOR,
                                                     'button[type="submit"]')
            submit_button.click()

    def _open_instagram(self):
        """ Navigate to Instagram and wait for the page to load. """
        self.driver.get('https://instagram.com')


insta_bot = InstaBot(username=4079029897, password='na!')
