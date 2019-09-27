from App.Models.facebookUser import FacebookUser


def scrape_like(driver, isTimelineLayout: bool) -> int:
    if(isTimelineLayout):
        likeNumber = 0
    else:
        likeNumber = driver.find_element_by_xpath("//*[@id='pages_side_column']//div[@class='_4-u2 _6590 _3xaf _4-u8']/div[3]").text
        likeNumber = likeNumber.split(' ', 1)[0].replace(',', '').replace('.', '')
    print(f"Likes: {likeNumber}")

    return likeNumber
