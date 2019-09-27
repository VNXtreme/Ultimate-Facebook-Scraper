from selenium.common.exceptions import NoSuchElementException


def scrape_profile_picture(driver, isTimelineLayout: bool):
    if isTimelineLayout:
        pictureURL = driver.find_element_by_xpath(".//div[@class='photoContainer']//img").get_attribute('src')
    else:
        try:
            pictureURL = driver.find_element_by_xpath(".//div[@class='_6tay']/img").get_attribute('src')
        except NoSuchElementException:
            pictureURL = driver.find_element_by_xpath(".//img[@class='_4jhq img']").get_attribute('src')
    
    return pictureURL
