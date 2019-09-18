def scrape_profile_picture(driver, isTimelineLayout: bool):
    if isTimelineLayout:
        pictureURL = driver.find_element_by_xpath(".//div[@class='photoContainer']/div/a/img").get_attribute('src')
    else:
        pictureURL = driver.find_element_by_xpath(".//div[@class='_6tay']/img").get_attribute('src')
    
    return pictureURL
