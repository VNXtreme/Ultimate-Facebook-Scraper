def scrape_name(driver, isTimelineLayout: bool) -> str:
    if(isTimelineLayout):
        fullnameElement = driver.find_element_by_id('fb-timeline-cover-name')
    else:
        fullnameElement = driver.find_element_by_xpath("//*[@id='seo_h1_tag']/a/span")
    name = fullnameElement.text
    print(f"Name: {name}")
        
    return name

def scrape_username(driver, isTimelineLayout: bool) -> str:
    if(isTimelineLayout):
        fullUrl = driver.find_element_by_xpath('//span[@id="fb-timeline-cover-name"]/a').get_attribute('href')
    else:
        fullUrl = driver.find_element_by_xpath("//*[@id='seo_h1_tag']/a").get_attribute('href')
    username = fullUrl.split('facebook.com')[1].replace('/', '')
    print(f"Username: {username}")
        
    return username
