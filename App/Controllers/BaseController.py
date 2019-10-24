import calendar
import os
import platform
import sys
import time
import urllib.request

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# from Database.facebookPost import FacebookPost
# from Database.facebookUser import FacebookUser
# # -------------------------------------------------------------
# from Functions.common import is_timeline_layout
# from Functions.follower import scrape_follower
# from Functions.isVerified import is_verified
# from Functions.like import scrape_like
# from Functions.name import scrape_name, scrape_username
# from Functions.posts import scrape_posts
# from Functions.profilePicture import scrape_profile_picture


class BaseController():
    driver = None

    def create_original_link(self, url):
        if url.find(".php") != -1:
            original_link = "https://en-gb.facebook.com/" + \
                ((url.split("="))[1])

            if original_link.find("&") != -1:
                original_link = original_link.split("&")[0]

        elif url.find("fnr_t") != -1:
            original_link = "https://en-gb.facebook.com/" + \
                ((url.split("/"))[-1].split("?")[0])
        elif url.find("_tab") != -1:
            original_link = "https://en-gb.facebook.com/" + \
                (url.split("?")[0]).split("/")[-1]
        else:
            original_link = url

        return original_link

    def check_page_existance(self, driver) -> bool:
        try:
            driver.find_element_by_xpath(
                './/i[contains(@class, "uiHeaderImage img")]')
            return False
        except NoSuchElementException:
            try:
                driver.find_element_by_xpath(
                    './/div[@class="pvl _4-do"]/h2[@class="_4-dp"]')
                return False
            except NoSuchElementException:
                return True

    def safe_find_element_by_id(self, driver, elem_id):
        try:
            return driver.find_element_by_id(elem_id)
        except NoSuchElementException:
            return None

    def load_driver(self):
        options = Options()
        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("user-data-dir=C:\\Users\\Xtreme\\AppData\\Local\\Google\\Chrome\\User Data1") #Path to your chrome profile C:\Users\Xtreme\AppData\Local\Google\Chrome\User Data
        # options.add_argument('profile-directory=Default1')
        # options.add_argument("headless")

        try:
            platform_ = platform.system().lower()
            if platform_ in ['linux', 'darwin']:
                self.driver = webdriver.Chrome(
                    executable_path="./chromedriver", options=options)
            else:
                self.driver = webdriver.Chrome(
                    executable_path="./chromedriver.exe", options=options)

        except:
            print("Kindly replace the Chrome Web Driver with the latest one from "
                  "http://chromedriver.chromium.org/downloads "
                  "and also make sure you have the latest Chrome Browser version."
                  "\nYour OS: {}".format(platform_)
                  )
            exit()

    def login(self, email, password):
        """ Logging into our own profile """

        try:
            self.load_driver()

            self.driver.get("https://en-gb.facebook.com")
            self.driver.maximize_window()

            if(self.driver.find_element_by_name('email')):
                # filling the form
                self.driver.find_element_by_name('email').send_keys(email)
                self.driver.find_element_by_name('pass').send_keys(password)

                # clicking on login button
                try:
                    self.driver.find_element_by_xpath(
                        '//button[@name="login"]').click()
                except NoSuchElementException:
                    self.driver.find_element_by_id('loginbutton').click()

                # if your account uses multi factor authentication
                mfa_code_input = self.safe_find_element_by_id(
                    self.driver, 'approvals_code')

                if mfa_code_input is None:
                    return

                mfa_code_input.send_keys(input("Enter MFA code: "))
                self.driver.find_element_by_id('checkpointSubmitButton').click()

                # there are so many screens asking you to verify things. Just skip them all
                while self.safe_find_element_by_id(self.driver, 'checkpointSubmitButton') is not None:
                    dont_save_browser_radio = self.safe_find_element_by_id(
                        self.driver, 'u_0_3')
                    if dont_save_browser_radio is not None:
                        dont_save_browser_radio.click()

                    self.driver.find_element_by_id(
                        'checkpointSubmitButton').click()

        except Exception as e:
            print("There's some error in log in.")
            print(sys.exc_info()[0])
            exit()
