def is_verified(driver, isTimelineLayout: bool):
    try:
        if(isTimelineLayout):
            driver.find_element_by_xpath('//div[@id="fbProfileCover"]//*[contains(@class, "_5d-1")]')
        else:
            driver.find_element_by_xpath('//*[contains(@class, "_5d-1")]')
        print(f"Verified: True")
        return 1
    except:
        print(f"Verified: False")
        return 0
