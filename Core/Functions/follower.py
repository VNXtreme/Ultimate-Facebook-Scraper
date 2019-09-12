from Database.facebookUser import FacebookUser
from Functions.common import extract_fb_username, extract_follower_number


def scrape_follower(driver, id):
    section = '/about'
    elements_path = "//div[@class='_3yo1']/span/span"

    driver.get(id + section)
    element = driver.find_elements_by_xpath(elements_path)

    followerNumber = extract_follower_number(element[0].text)

    # update DB
    FBusername = extract_fb_username(id)
    update_follower_number(FBusername, followerNumber)

    return followerNumber


def update_follower_number(fbUsername, followerNumber):
    user, created = FacebookUser.get_or_create(
        username=fbUsername, defaults={'followers': followerNumber})
    if not created:
        user.followers = followerNumber
        user.save()
