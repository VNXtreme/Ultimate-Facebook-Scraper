from selenium.webdriver.support.ui import WebDriverWait

from App.Controllers.Functions.common import safely_generate_url


def scrape_gender(driver, fullUrl, isTimelineLayout):
    WebDriverWait(driver, 2)
    navigateUrl = safely_generate_url(fullUrl, 'about?section=contact-info')
    driver.get(navigateUrl)

    try:
        if isTimelineLayout:
            return driver.find_element_by_xpath('//div[@id="pagelet_basic"]//ul/li[@class="_3pw9 _2pi4 _2ge8 _3ms8"]//div[@class="_4bl7 _pt5"]//span[@class="_2iem"]').text
        else:
            return driver.find_element_by_xpath('//*[contains(text(), "Giới tính")]//following-sibling::div').text
    except:
        return None


def scrape_biology(driver, fullUrl, isTimelineLayout):
    WebDriverWait(driver, 2)
    navigateUrl = safely_generate_url(fullUrl, 'about?section=bio')
    if driver.current_url != navigateUrl:
        driver.get(navigateUrl)

    try:
        if isTimelineLayout:
            try:
                driver.find_element_by_xpath(
                    '//div[@id="pagelet_bio"]//ul/li/span[@class="_50f8 _2iem"]').text # if element exist, no biology info
                return None
            except:
                return driver.find_element_by_xpath('//div[@id="pagelet_bio"]//ul/li').text
        else:
            return driver.find_element_by_xpath('//*[contains(text(), "Tiểu sử")]//following-sibling::div').text
    except:
        return None

def scrape_about(driver, fullUrl, isTimelineLayout):
    WebDriverWait(driver, 2)
    navigateUrl = safely_generate_url(fullUrl, 'about?section=bio')
    if driver.current_url != navigateUrl:
        driver.get(navigateUrl)

    try:
        if isTimelineLayout:
            try:
                driver.find_element_by_xpath(
                    '//div[@id="pagelet_bio"]//ul/li/span[@class="_50f8 _2iem"]').text # if element exist, no biology info
                return None
            except:
                return driver.find_element_by_xpath('//div[@id="pagelet_bio"]//ul/li').text
        else:
            return driver.find_element_by_xpath('//div[@class="_1xnd"]//*[contains(text(), "Giới thiệu")]//following-sibling::div').text
    except:
        return None

def scrape_location(driver, fullUrl, isTimelineLayout):
    WebDriverWait(driver, 2)
    location = None
    navigateUrl = safely_generate_url(fullUrl, 'about?section=living')

    if driver.current_url != navigateUrl:
        driver.get(navigateUrl)

    try:
        if isTimelineLayout:
            try:
                location = driver.find_element_by_xpath('//li[@id="current_city"]//span[@class="_2iel _50f7"]').text
            except:
                location = driver.find_element_by_xpath('//li[@id="hometown"]//span[@class="_2iel _50f7"]').text
        else:
            try:
                location = driver.find_element_by_xpath('//div[@class="_1xnd"]//*[contains(text(), "Vị trí hiện tại")]//following-sibling::div').text
            except:
                location = driver.find_element_by_xpath('//div[@class="_1xnd"]//*[contains(text(), "Quê quán")]//following-sibling::div').text
         
        return filter_location_name(location)
    except:
        return None

def filter_location_name(location):
    arrayHCM = ['Hồ Chí Minh', 'HCM']
    arrayHanoi = ['Hà Nội', 'hanoi']

    if any(name in location for name in arrayHanoi):
        return 'Hà Nội'
    elif any(name in location for name in arrayHCM):
        return 'Hồ Chí Minh'
    else:
        return location
