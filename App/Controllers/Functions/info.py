from App.Controllers.Functions.common import safely_generate_url


def scrape_gender(driver, fullUrl, isTimelineLayout):
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
    navigateUrl = safely_generate_url(fullUrl, 'about?section=bio')
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
    navigateUrl = safely_generate_url(fullUrl, 'about?section=bio')
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
