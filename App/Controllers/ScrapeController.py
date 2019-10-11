# import calendar
# import os
# import platform
# import sys
# import time
# import urllib.request

# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

from App.Controllers.BaseController import BaseController
from App.Models.facebookPost import FacebookPost
from App.Models.facebookUser import FacebookUser

# -------------------------------------------------------------
from .Functions.common import is_timeline_layout
from .Functions.follower import scrape_follower
from .Functions.info import scrape_gender
from .Functions.isVerified import is_verified
from .Functions.like import scrape_like
from .Functions.name import scrape_name, scrape_username
from .Functions.posts import scrape_posts
from .Functions.profilePicture import scrape_profile_picture


class ScrapeController(BaseController):
    PREFIX_URL = "https://en-gb.facebook.com/"

    def run(self, listFbUsername=None):
        if not listFbUsername:
            listFbUsername = self.list_fb_username_from_file()

        if len(listFbUsername) > 0:
            print("\nStarting Scraping...")

            self.login_facebook_on_browser()
            self.scrape_elements(listFbUsername)
            self.driver.close()
            return 'Done'
        else:
            print("Input file is empty.")

    def list_fb_username_from_file(self) -> list:
        return [line.rstrip('\r\n') for line in open("Input/input.txt", newline='\r\n')]

    def login_facebook_on_browser(self):
        with open('Input/credentials.txt') as f:
            email = f.readline().split('"')[1]
            password = f.readline().split('"')[1]

            if email == "" or password == "":
                print(
                    "Your email or password is missing. Kindly write them in credentials.txt")
                exit()

        self.login(email, password)

    def scrape_elements(self, listFbUsername):
        # execute for all profiles given in input.txt file
        for index, fbUsername in enumerate(listFbUsername):
            # STOP if too many profile
            if (index > 150):
                print('Over 150 profiles. Exit.')
                break

            self.driver.get(self.PREFIX_URL + fbUsername)
            url = self.driver.current_url
            fullUrl = self.create_original_link(url)

            print("----------------Start---------------------")
            exist = self.check_page_existance(self.driver)
            if not exist:
                print(f'Page not exist: {fbUsername}')
                print('----------------Skip---------------------\n')
                continue

            print(f"Scraping: {fbUsername}")
            isTimelineLayout = is_timeline_layout(self.driver)  # check layout

            # scrape
            username = scrape_username(self.driver, isTimelineLayout)
            isVerified = is_verified(self.driver, isTimelineLayout)
            name = scrape_name(self.driver, isTimelineLayout)
            profilePictureURL = scrape_profile_picture(
                self.driver, isTimelineLayout)
            followerNumber = scrape_follower(self.driver, isTimelineLayout)
            likeNumber = scrape_like(self.driver, isTimelineLayout)

            fbPosts = scrape_posts(self.driver, fullUrl, isTimelineLayout)

            gender = scrape_gender(self.driver, fullUrl, isTimelineLayout)
            # print(gender)

            user = FacebookUser.update_or_create(username, {
                'followers': followerNumber,
                'likes': likeNumber,
                'name': name,
                'gender': gender,
                'profile_picture_url': profilePictureURL,
                'is_private': isTimelineLayout and 1 or 0,
                'is_verified': isVerified
            })
            FacebookPost.update_or_create_fbpost(user.id, fbPosts)

            print("----------------Done---------------------\n")
            # ----------------------------------------------------------------------------

        print("\nProcess Completed.")

        return

    def scrape_by_username(self, username):
        listFbUsername = [username]
        self.run(listFbUsername)

        return 'Done '+username
