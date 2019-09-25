from Database.facebookUser import FacebookUser


def scrape_follower(driver, isTimelineLayout: bool) -> int:
    try:
        if(isTimelineLayout):
            followerNumber = driver.find_element_by_xpath("//div[@class='_6a _6b plm']/span").text
        else:
            followerNumber = driver.find_element_by_xpath("//*[@id='pages_side_column']//div[@class='_4-u2 _6590 _3xaf _4-u8']/div[4]").text
        followerNumber = followerNumber.split(' ', 1)[0].replace(',', '').replace('.', '')
    except:
        followerNumber = 0
    print(f"Followers: {followerNumber}")

    return followerNumber
