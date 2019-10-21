from datetime import datetime

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from App.Controllers.Functions.common import safely_generate_url

total_scrolls = 2
scroll_time = 5
old_height = 0


def scrape_posts(driver, fbUrl, isTimelineLayout: bool):
    if isTimelineLayout:
        driver.get(fbUrl)
        scroll(driver)
        elementPosts = driver.find_elements_by_xpath(
            '//div[@class="_5pcb _4b0l _2q8l"]')
        return extract_posts(elementPosts, driver)

    else:
        newUrl = safely_generate_url(fbUrl, 'posts')
        driver.get(newUrl)
        scroll(driver)

        elementPosts = driver.find_elements_by_xpath(
            '//div[@id="pagelet_timeline_main_column"]//div[@class="_4-u2 _4-u8"]')
        return extract_posts(elementPosts, driver)


def extract_posts(elements, driver) -> list:
    try:
        posts = []
        for postElement in elements:
            try:
                title = get_title(postElement)
                time = get_time(postElement)
                link = get_link(postElement)
                
                postMessage = post_message(postElement)
                postImage = post_image(postElement)

                totalReaction = total_reaction(postElement)
                comments = total_comment(postElement)
                shares = total_share(postElement)
                
                open_reaction_popup(postElement, driver)
                likes = total_like(driver)
                loves = total_love(driver)
                hahas = total_haha(driver)
                wows = total_wow(driver)
                sads = total_sad(driver)
                angers = total_anger(driver)
                print(likes, loves, hahas, wows, sads, angers)
                close_reaction_popup(postElement, driver)
                reactions = [
                    likes,
                    loves,
                    hahas,
                    wows,
                    sads,
                    angers,
                    totalReaction,
                    comments,
                    shares
                ]
                posts.append(
                    [link, postMessage, postImage, time, title, reactions])

            except Exception as extractError:
                print('extract loop: ', extractError)
        return posts
    except NoSuchElementException as e:
        print("Exception (extract_posts)",
              "Status =", e)

    return


def get_link(driver) -> str:
    prefix = 'https://www.facebook.com'
    try:
        linkElement = driver.find_element_by_tag_name(
            'abbr').find_element_by_xpath(".//ancestor::a")
    except NoSuchElementException:
        return None

    # link = linkElement.get_attribute('ajaxify')

    # if link is None:
    link = linkElement.get_attribute('href')
    # link = link.split('__xts__')[0][:-1]
    # if(link[0] == '/'):
    link = link.split('__xts__')[
        0][:-1] if link.find('__xts__') != -1 else link
    link = (prefix + link) if link[0] == '/' else link

    return link

def total_reaction(element) -> str:
    try:
        return element.find_element_by_xpath('.//span[@class="_3dlg"]/span/span').text
    except NoSuchElementException:
        return 0


def total_comment(element) -> str:
    try:
        return element.find_element_by_xpath('.//a[@data-testid="UFI2CommentsCount/root"]').text
    except NoSuchElementException:
        return 0


def total_share(element) -> str:
    try:
        return element.find_element_by_xpath('.//a[@data-testid="UFI2SharesCount/root"]').text
    except NoSuchElementException:
        return 0


def post_message(element) -> str:
    try:
        return element.find_element_by_xpath('.//div[contains(@class, "_5pbx userContent")]').text
    except NoSuchElementException:
        return None


def post_image(element) -> str:
    try:
        return element.find_element_by_xpath('.//img[@class="_3chq"]').get_attribute('src')
    except NoSuchElementException:
        try:
            return element.find_element_by_xpath('.//div[@class="_3x-2"]//img[contains(@class,"img")]').get_attribute('src')
        except NoSuchElementException:
            return None


def get_title(element) -> str:
    try:
        return element.find_element_by_xpath(".//span[@class='fwb fcg']").text
    except:
        try:
            return element.find_element_by_xpath(".//span[@class='fwn fcg']").text
        except:
            return ''


def get_time(element) -> str:
    try:
        timestamp = element.find_element_by_tag_name(
            'abbr').get_attribute('data-utime')
        return timestamp
    except:
        return ''


def scroll(driver):
    global old_height
    current_scrolls = 0

    while (True):
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script(
                "return document.body.scrollHeight")
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(
                lambda driver: check_height(driver))
            current_scrolls += 1
        except TimeoutException:
            break

    return


def check_height(driver) -> bool:
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


def open_reaction_popup(element, driver):
    try:
        element.find_element_by_xpath('.//span[@class="_1n9r _66lh"]/span/a')
        WebDriverWait(driver, 2).until(EC.invisibility_of_element_located((By.XPATH, '//span[@class="_1n9r _66lh"]/span/a')))
    except:
        pass

    popupElement = element.find_element_by_xpath('.//span[@class="_1n9r _66lh"]/span/a')
    driver.execute_script("arguments[0].click();", popupElement)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_59s7"]//div[@class="_4-i2 _50f4"]//ul[@class="_43o4 _4470"]')))
    

def total_like(element) -> str:
    try:
        return element.find_element_by_xpath('//div[@class="_59s7"]//div[@class="_4-i2 _50f4"]//ul[@class="_43o4 _4470"]//i[contains(@class,"sx_07ad5e")]/ancestor::a[@class="_3m1v _468f"]').text
    except NoSuchElementException:
        return 0

def total_haha(element) -> str:
    try:
        return element.find_element_by_xpath('//div[@class="_59s7"]//div[@class="_4-i2 _50f4"]//ul[@class="_43o4 _4470"]//i[contains(@class,"sx_e1f302")]/ancestor::a[@class="_3m1v _468f"]').text
    except NoSuchElementException:
        return 0

def total_sad(element) -> str:
    try:
        return element.find_element_by_xpath('//div[@class="_59s7"]//div[@class="_4-i2 _50f4"]//ul[@class="_43o4 _4470"]//i[contains(@class,"sx_8d23c2")]/ancestor::a[@class="_3m1v _468f"]').text
    except NoSuchElementException:
        return 0

def total_anger(element) -> str:
    try:
        return element.find_element_by_xpath('//div[@class="_59s7"]//div[@class="_4-i2 _50f4"]//ul[@class="_43o4 _4470"]//i[contains(@class,"sx_162385")]/ancestor::a[@class="_3m1v _468f"]').text
    except NoSuchElementException:
        return 0

def total_wow(element) -> str:
    try:
        return element.find_element_by_xpath('//div[@class="_59s7"]//div[@class="_4-i2 _50f4"]//ul[@class="_43o4 _4470"]//i[contains(@class,"sx_8b39f1")]/ancestor::a[@class="_3m1v _468f"]').text
    except NoSuchElementException:
        return 0

def total_love(element) -> str:
    try:
        return element.find_element_by_xpath('//div[@class="_59s7"]//div[@class="_4-i2 _50f4"]//ul[@class="_43o4 _4470"]//i[contains(@class,"sx_24e654")]/ancestor::a[@class="_3m1v _468f"]').text
    except NoSuchElementException:
        return 0

def close_reaction_popup(element, driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'layerCancel')))
    popupCloseButton = element.find_element_by_xpath('//div[@class="_59s7"]//*[contains(@class,"layerCancel")]')
    driver.execute_script("arguments[0].click();", popupCloseButton)
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="_59s7"]//*[contains(@class,"layerCancel")]')))
    # driver.find_element_by_xpath('//a[contains(@class,"layerCancel")]').click()
