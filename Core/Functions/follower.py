from Database.facebookUser import FacebookUser
from Functions.common import extract_fb_username, extract_follower_number


def scrape_follower(driver, id, isTimelineLayout):
    driver.get(id)

    if(isTimelineLayout):
        elementPath = "//div[@class='_6a _6b plm']/span"
        element = driver.find_element_by_xpath(elementPath)
        followerNumber = element.text.split(' ', 1)[0].replace(',', '')
    else:
        elementPath = "//div[@class='_1nq8  _2ieq']"
        element = driver.find_element_by_xpath(elementPath)
        followerNumber = element.text.split(' ', 3)[2].replace(',', '')

    # update DB
    # FBusername = extract_fb_username(id)
    # update_follower_number(FBusername, followerNumber)
    # FacebookUser.update_or_create(FBusername, followerNumber)

    return followerNumber


# def update_follower_number(fbUsername, followerNumber):
#     user, created = FacebookUser.get_or_create(
#         username=fbUsername, defaults={'followers': followerNumber})
#     if not created:
#         user.followers = followerNumber
#         user.save()
