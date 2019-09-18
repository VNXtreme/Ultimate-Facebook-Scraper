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

from Database.facebookPost import FacebookPost
from Database.facebookUser import FacebookUser
# -------------------------------------------------------------
from Functions.common import extract_fb_username, is_timeline_layout
from Functions.follower import scrape_follower
from Functions.name import scrape_name
from Functions.posts import scrape_posts
from Functions.profilePicture import scrape_profile_picture

# -------------------------------------------------------------


# -------------------------------------------------------------


# Global Variables
prefixUrl = "https://en-gb.facebook.com/"
driver = None

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def create_original_link(url):
    if url.find(".php") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("="))[1])

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


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def safe_find_element_by_id(driver, elem_id):
    try:
        return driver.find_element_by_id(elem_id)
    except NoSuchElementException:
        return None


def login(email, password):
    """ Logging into our own profile """

    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")

        try:
            platform_ = platform.system().lower()
            if platform_ in ['linux', 'darwin']:
                driver = webdriver.Chrome(
                    executable_path="./chromedriver", options=options)
            else:
                driver = webdriver.Chrome(
                    executable_path="./chromedriver.exe", options=options)
        except:
            print("Kindly replace the Chrome Web Driver with the latest one from "
                  "http://chromedriver.chromium.org/downloads "
                  "and also make sure you have the latest Chrome Browser version."
                  "\nYour OS: {}".format(platform_)
                  )
            exit()

        driver.get("https://en-gb.facebook.com")
        driver.maximize_window()

        # filling the form
        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('pass').send_keys(password)

        # clicking on login button
        driver.find_element_by_id('loginbutton').click()

        # if your account uses multi factor authentication
        mfa_code_input = safe_find_element_by_id(driver, 'approvals_code')

        if mfa_code_input is None:
            return

        mfa_code_input.send_keys(input("Enter MFA code: "))
        driver.find_element_by_id('checkpointSubmitButton').click()

        # there are so many screens asking you to verify things. Just skip them all
        while safe_find_element_by_id(driver, 'checkpointSubmitButton') is not None:
            dont_save_browser_radio = safe_find_element_by_id(driver, 'u_0_3')
            if dont_save_browser_radio is not None:
                dont_save_browser_radio.click()

            driver.find_element_by_id('checkpointSubmitButton').click()

    except Exception as e:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit()


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def main():
    with open('Input/credentials.txt') as f:
        email = f.readline().split('"')[1]
        password = f.readline().split('"')[1]

        if email == "" or password == "":
            print(
                "Your email or password is missing. Kindly write them in credentials.txt")
            exit()

    listFbUsername = [line for line in open("Input/input.txt", newline='\n')]
    
    if len(listFbUsername) > 0:
        print("\nStarting Scraping...")

        login(email, password)
        start_scape(listFbUsername)
        driver.close()
    else:
        print("Input file is empty.")


def start_scape(listFbUsername):
    # execute for all profiles given in input.txt file
    for fbUsername in listFbUsername:
        driver.get(prefixUrl+fbUsername)
        url = driver.current_url
        fullUrl = create_original_link(url)
        
        print("\nScraping:", fbUsername)
        print("----------------------------------------")
        isTimelineLayout = is_timeline_layout(driver)  # check layout

        # scrape
        # profilePictureURL = scrape_profile_picture(driver, isTimelineLayout)
        # name = scrape_name(driver, isTimelineLayout)
        # followerNumber = scrape_follower(driver, id, isTimelineLayout)
        fbPosts = scrape_posts(driver, fullUrl, isTimelineLayout)
        # print('post', "\n", fbPosts)

        # update DB
        # fbUsername = extract_fb_username(id)
        # FacebookUser.update_or_create(fbUsername, {
        #     'followers': followerNumber,
        #     'name': name,
        #     'profile_picture_url': profilePictureURL
        # })
        FacebookPost.update_or_create_fbpost(fbPosts)

        print("----------------Done---------------------")
        # ----------------------------------------------------------------------------

    print("\nProcess Completed.")

    return

# -------------------------------------------------------------
# -------------------------------------------------------------


if __name__ == '__main__':
    # get things rolling
    main()
