#!/usr/bin/env python3

import sys
from getopt import getopt, GetoptError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from urllib3.exceptions import ProtocolError

from time import sleep


class InstaBot:
    def __init__(self, username, password, target, mode='headless'):
        """
            Get an instance of a web browser, login to Instagram and start auto-liking.\n

            :arg
                -   username:   Phone number, email, whatever you use to login to Instagram.
                -   password:   Your Instagram password associated with the username.
                -   target:     Instagram username whose posts you want to like.
                -   mode:       Can be "visible" for a visible browser or "headless" for no
                                visible browser.
        """

        # InstaBot instance variables.
        # Constants.
        self.driver = None
        if mode == 'visible':
            self.driver = webdriver.Firefox(executable_path='./geckodriver')
        elif mode == 'headless':
            ff_options = Options()
            ff_options.add_argument('--headless')
            self.driver = webdriver.Firefox(executable_path='./geckodriver',
                                            options=ff_options)
        self.wait = WebDriverWait(self.driver, 10)  # Wait functionality.
        self.url = 'https://instagram.com'
        # Variable: User dependant.
        self.username = str(username)  # Instagram login username.
        self.password = str(password)  # Instagram password.
        self.target = str(target)  # Instagram username of the target whose posts you want to like.

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
            try:
                if self._find_user():
                    self._like_posts()
                    # Sleep for one hour before checking again.
                    sleep(60 * 60)
            except (KeyboardInterrupt,
                    ElementClickInterceptedException,
                    ConnectionResetError,
                    ConnectionAbortedError,
                    ProtocolError):
                self.end_session()

    def _disable_notifications(self):
        """
            Look for the enable notifications pop-up. Respond with disable.
        """
        if self._wait_until(e_c.presence_of_element_located, By.XPATH, '//div[@role="dialog"]'):
            notifications = self.driver.find_element(By.XPATH, '//div[@role="dialog"]')
            # If the pop-up is found, click Not Now to notifications.
            notifications.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()

    def _find_user(self):
        """
            Find a user and navigate to their page.\n

            :arg
                -   user:   A string of the username of the user you intend to find.
            :returns
                -   True if the target user was found and navigated to.
        """
        if self._wait_until(e_c.presence_of_element_located, By.CSS_SELECTOR,
                            'input[placeholder="Search"'):
            search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search"')
            search_bar.clear()
            search_bar.send_keys(self.target)
            if self._wait_until(e_c.presence_of_element_located,
                                By.CSS_SELECTOR, 'a[href="/' + self.target + '/"]'):
                self.driver.get('/'.join([self.url, self.target]))
                return True
            else:
                self.end_session(message='Target user not found.')

    def _like_posts(self):
        """
            Gets the page hyperlink of each image on an Instagram user's profile, navigates to
            those urls, and clicks the like button if the photo is not already liked.
        """
        if self._wait_until(e_c.presence_of_all_elements_located, By.CSS_SELECTOR, 'article'):
            posts = self.driver.find_elements(By.CSS_SELECTOR, 'article a')
            posts = [post.get_attribute('href') for post in posts]
            for post in posts:
                self.driver.get(post)
                if self._wait_until(e_c.presence_of_all_elements_located, By.CSS_SELECTOR,
                                    'button svg[width="24"]'):
                    try:
                        like_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                                                 'button svg[width="24"]')
                    except NoSuchElementException:
                        pass
                    else:
                        for like_button in like_buttons:
                            if 'Like' in like_button.get_attribute('aria-label'):
                                like_button.click()

    def _login(self):
        """
            Type the username and password into their respective fields and click the submit
            button.\n

            :returns
                -   True on success of _login() attempt.
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
            self.end_session()

    def _open_instagram(self):
        """
            Navigate to Instagram and wait for the page to load.\n

            :returns
                -   True on success of self.driver.get(self.url).
            :raises
                -   selenium.common.exceptions.WebDriverException
        """
        try:
            self.driver.get(self.url)
        except WebDriverException:
            self.end_session(message="Instagram wasn't able to open for some reason...check your "
                                     "internet connection?")
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
            return False
        else:
            return True

    def end_session(self, message=None):
        """
            End the current session of InstaBot displaying a browser alert if certain errors
            occur. Browser alert will only appear if utilizing the geckodriver browser.\n

            :arg
                -   message:    Message of what went wrong to display to the user in visible
                                operation mode.
        """
        if message is not None:
            self.driver.execute_script(
                'window.alert("' + str(message) + '\\nWaiting 10 seconds before exit.");'
            )
        else:
            self.driver.execute_script(
                'window.alert("Something went wrong.\\nWaiting 10 seconds before exit.");'
            )
        sleep(10)
        self.driver.close()
        self.driver.quit()
        exit(0)


if __name__ == '__main__':
    usage_message = """
                main.py -u <username> -p <password> -t <target> -m <mode>
                \n\n\t\tor\n\n
                main.py --username <username> --password <password> --target <target> --mode <mode>
                -   username:   Phone number, email, whatever you use to login to Instagram.
                -   password:   Your Instagram password associated with the username.
                -   target:     Instagram username whose posts you want to like.
                -   mode:       Can be "visible" for a FireFox browser or "headless" for no 
                                visible browser.
                """
    un, pw, t, m = None, None, None, None
    try:
        options, throw_away = getopt(sys.argv[1:], 'u:p:t:m:',
                                     ['username=', 'password=', 'target=', 'mode='])
    except GetoptError:
        print(usage_message)
        sys.exit(2)
    else:
        if len(options) == 3 or len(options) == 4:
            for option, argument in options:
                if option not in \
                        ['-u', '-p', '-t', '-m', '--username', '--password', '--target', '--mode']:
                    print(usage_message)
                    sys.exit()
                elif option in ('-u', '--username'):
                    un = argument
                elif option in ('-p', '--password'):
                    pw = argument
                elif option in ('-t', '--target'):
                    t = argument
                elif option in ('-m', '--mode'):
                    m = argument
            if m is not None:
                InstaBot(username=un, password=pw, target=t, mode=m)
            else:
                InstaBot(username=un, password=pw, target=t)
        else:
            print(usage_message)
            sys.exit()
