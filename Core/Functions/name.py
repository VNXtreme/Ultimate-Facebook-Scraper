def scrape_name(driver, isTimelineLayout):
    if(isTimelineLayout):
        fullnameElement = driver.find_element_by_id('fb-timeline-cover-name')
    else:
        fullnameElement = driver.find_element_by_xpath("//*[@id='seo_h1_tag']/a/span")
    fullname = fullnameElement.text
        
    return fullname
