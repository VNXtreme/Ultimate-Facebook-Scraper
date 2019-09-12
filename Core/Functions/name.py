def getName(driver):
    fullnameElement = safe_find_element_by_id(driver, 'fb-timeline-cover-name')
    if fullnameElement:
        fullname = fullnameElement.text
    else:
        fullnameElement = driver.find_elements_by_xpath("//*[@id='seo_h1_tag']/a/span")
        fullname = fullnameElement[0].text
