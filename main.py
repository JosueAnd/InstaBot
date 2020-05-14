from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep


class InstaBot:
    def __init__(self, username, password, target):
        """
            Get an instance of a web browser, login to Instagram and start auto-liking.\n

            :arg
                -   username:   Phone number, email, whatever you use to login to Instagram.
                -   password:   Your Instagram password associated with the username.
                -   target:     Instagram username whose posts you want to like.
        """

        # InstaBot instance variables.
        # Constants.
        self.driver = webdriver.Firefox(executable_path='./geckodriver')    # Firefox web browser.
        self.wait = WebDriverWait(self.driver, 10)  # Wait functionality.
        self.action_chain = ActionChains(self.driver)
        self.url = 'https://instagram.com'
        # Variable: User dependant.
        self.username = str(username)   # Instagram login username.
        self.password = str(password)   # Instagram password.
        self.target = str(target)   # Instagram username of the target whose posts you want to like.

        # Opening Instagram page, logging in and enabling pop-ups.
        if self._open_instagram():
            if self._login():
                self._disable_notifications()
                self._open_new_tab()
                # self.run()

    def run(self):
        """
            Run the script indefinitely.
        """
        while True:
            try:
                if self._find_user():
                    self._like_posts()
                    # Sleep for one hour before checking again.
                    sleep(5)
            except KeyboardInterrupt:
                self.end_session()

    def _disable_notifications(self):
        """
            Look for the enable notifications pop-up. Respond with disable.
        """
        if self._wait_until(e_c.presence_of_element_located, By.XPATH, '//div[@role="dialog"]'):
            notifications = self.driver.find_element(By.XPATH, '//div[@role="dialog"]')
            # If the pop-up is found, click Not Now to notifications.
            notifications.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()

    def _disable_obscures(self):
        """
            Sometimes there are these invisible elements that obscure links on the screen,
            preventing you from clicking them, or preventing selenium from clicking them and they
            cause a selenium.common.exceptions.ElementClickIntercepted Exception. Pretty annoying,
            so this method is to delete them and circumvent the issue.

            source: https://www.geeksforgeeks.org/how-to-remove-an-html-element-using-javascript/
        """
        # FIXME:    May deprecate this method. Even deleting the obscuring element does not allow us
        #           to click underlying elements so this method might be pointless.
        if self._wait_until(e_c.presence_of_all_elements_located, By.CLASS_NAME, 'jLwSh'):
            self.driver.execute_script("""
                let pain = document.getElementsByClassName('jLwSh');
                for (let x = 0; x < pain.length; x++) {
                    pain[x].parentNode.removeChild(pain[x]);
                }
            """)

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
        # TODO: add documentation
        if self._wait_until(e_c.presence_of_all_elements_located, By.CSS_SELECTOR, 'article a'):
            """
                Alright guys, new plan. It seems instagram makes it extremely difficult to automate
                using elements and clicks directly, probably to eliminate: scrapers, bots, etc., so
                to get around this we are going to open pages using the href links of the elements
                we want to like. So what we need to do is figure out in selenium how to open and 
                manage multiple windows and then close multiple windows. We may need to work out 
                a new workflow to ensure the entire browser is not closed.
            """
            pass
            # posts = self.driver.find_elements(By.CSS_SELECTOR, 'article a')
            # for post in posts:
            #     post.click()
            #     if self._wait_until(e_c.presence_of_element_located, By.CSS_SELECTOR,
            #                          'button svg[aria-label*="like"]'):
            #         try:
            #             like_button = post.find_element(By.CSS_SELECTOR,
            #                                             'button svg[aria-label*="like"]')
            #         except NoSuchElementException:
            #             pass
            #         else:
            #             if 'Like' in like_button.get_attribute('aria-label'):
            #                 like_button.click()
            #             close_button = self.driver.find_element(By.CSS_SELECTOR,
            #                                     'button svg[aria-label="Close"]')
            #             close_button.click()

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

    def _open_new_tab(self):
        # TODO: add documentation
        # self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        new_tab = self.action_chain.key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL)
        new_tab.perform()

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
        # TODO: add documentation
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


# Actual goal of calling InstaBot.
insta_bot = InstaBot(username=4079029897, password='na!', target='creativesoulmedia')
# Tester call on InstaBot.
# insta_bot = InstaBot(username=4079029897, password='Josue1234!', target='hello_mojo_no_real_go')
