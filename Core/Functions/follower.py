from Database.facebookUser import FacebookUser
from Functions.common import extract_fb_username, extract_follower_number


def scrape_follower(driver, fbUrl: str, isTimelineLayout: bool) -> int:
    driver.get(fbUrl)

    if(isTimelineLayout):
        elementPath = "//div[@class='_6a _6b plm']/span"
        element = driver.find_element_by_xpath(elementPath)
        followerNumber = element.text.split(' ', 1)[0].replace(',', '')
    else:
        elementPath = "//div[@class='_1nq8  _2ieq']"
        element = driver.find_element_by_xpath(elementPath)
        followerNumber = element.text.split(' ', 3)[2].replace(',', '')

    print(f"Followers: {followerNumber}")
    return followerNumber
