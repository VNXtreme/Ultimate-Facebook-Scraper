def scrape_name(driver, isTimelineLayout: bool) -> str:
    if(isTimelineLayout):
        fullnameElement = driver.find_element_by_id('fb-timeline-cover-name')
    else:
        fullnameElement = driver.find_element_by_xpath("//*[@id='seo_h1_tag']/a/span")
    name = fullnameElement.text
    print(f"Name: {name}")
        
    return name
