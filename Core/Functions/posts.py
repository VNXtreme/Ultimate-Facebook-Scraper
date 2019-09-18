from datetime import datetime

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

total_scrolls = 10
scroll_time = 5
old_height = 0


def scrape_posts(driver, fbUrl, isTimelineLayout: bool):
    if isTimelineLayout:
        scroll(driver)
        elementPosts = driver.find_elements_by_xpath(
            '//div[@class="_5pcb _4b0l _2q8l"]')
        return extract_timeline_posts(elementPosts)

    else:
        driver.get(fbUrl + '/posts')
        scroll(driver)
        # need update
        elementPosts = driver.find_elements_by_xpath(
            '//div[@class="_4-u2 _4-u8"]')
        return extract_timeline_posts(elementPosts)


def extract_timeline_posts(elements) -> list:
    try:
        posts = []
        for postElement in elements:
            try:
                title = get_title(postElement)
                time = get_time(postElement)
                link = get_link(postElement)
                # print(title, "\n")
                postMessage = post_message(postElement)
                postImage = post_image(postElement)

                likes = total_like(postElement)
                loves = total_love(postElement)
                hahas = total_haha(postElement)
                totalReaction = total_reaction(postElement)
                comments = total_comment(postElement)
                shares = total_share(postElement)

                reactions = [
                    likes,
                    loves,
                    hahas,
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
    linkElement = driver.find_element_by_tag_name(
        'abbr').find_element_by_xpath(".//ancestor::a")

    # link = linkElement.get_attribute('ajaxify')

    # if link is None:
    link = linkElement.get_attribute('href')

    if(link[0] == '/'):
        link = prefix + link

    return link


def total_like(element) -> str:
    try:
        return element.find_element_by_xpath('.//span[@data-testid="UFI2TopReactions/tooltip_LIKE"]/a').get_attribute('aria-label')
    except NoSuchElementException:
        return ''


def total_love(element) -> str:
    try:
        return element.find_element_by_xpath('.//span[@data-testid="UFI2TopReactions/tooltip_LOVE"]/a').get_attribute('aria-label')
    except NoSuchElementException:
        return ''


def total_haha(element) -> str:
    try:
        return element.find_element_by_xpath('.//span[@data-testid="UFI2TopReactions/tooltip_HAHA"]/a').get_attribute('aria-label')
    except NoSuchElementException:
        return ''


def total_reaction(element) -> str:
    try:
        return element.find_element_by_xpath('.//span[@class="_3dlg"]/span/span').text
    except NoSuchElementException:
        return ''


def total_comment(element) -> str:
    try:
        return element.find_element_by_xpath('.//a[@data-testid="UFI2CommentsCount/root"]').text
    except NoSuchElementException:
        return ''


def total_share(element) -> str:
    try:
        return element.find_element_by_xpath('.//a[@data-testid="UFI2SharesCount/root"]').text
    except NoSuchElementException:
        return ''


def post_message(element) -> str:
    try:
        return element.find_element_by_xpath('.//div[contains(@class, "_5pbx userContent")]').text
    except NoSuchElementException:
        return ''


def post_image(element) -> str:
    try:
        return element.find_element_by_xpath('.//div[@class="_3x-2"]').find_element_by_tag_name('img').get_attribute('src')
    except NoSuchElementException:
        # print("post_image error: " , e)
        return None


def get_title(x):
    title = ""
    try:
        title = x.find_element_by_xpath(".//span[@class='fwb fcg']/a").text
    except:
        try:
            title = x.find_element_by_xpath(".//span[@class='fcg']/a").text
        except:
            try:
                title = x.find_element_by_xpath(
                    ".//span[@class='fwn fcg']/span").text
            except:
                return ''
    finally:
        return title


def get_time(element):
    try:
        # time = element.find_element_by_tag_name('abbr').get_attribute('title')
        # time = str("%02d" % int(time.split(", ")[1].split()[1]), ) + "-" + str(
        #     ("%02d" % (int((list(calendar.month_abbr).index(time.split(", ")[1].split()[0][:3]))),))) + "-" + \
        #     time.split()[3] + " " + str("%02d" % int(time.split()[5].split(":")[0])) + ":" + str(
        #     time.split()[5].split(":")[1])
        timestamp = element.find_element_by_tag_name(
            'abbr').get_attribute('data-utime')
        return timestamp
        # print('time =', datetime.utcfromtimestamp(timestamp*1000).isoformat())
        # return datetime.utcfromtimestamp(timestamp).isoformat()
        # return element.find_element_by_tag_name('abbr').get_attribute('data-utime') #timestamp
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


def check_height(driver):
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


##
# if title.text == driver.find_element_by_id("fb-timeline-cover-name").text:
#     if status == '':
#         temp = get_div_links(x, "img")
#         if temp == '':  # no image tag which means . it is not a life event
#             link = get_div_links(x, "a").get_attribute('href')
#             type = "status update without text"
#         else:
#             type = 'life event'
#             link = get_div_links(x, "a").get_attribute('href')
#             status = get_div_links(x, "a").text
#     else:
#         type = "status update"
#         if get_div_links(x, "a") != '':
#             link = get_div_links(x, "a").get_attribute('href')

# elif title.text.find(" shared ") != -1:

#     x1, link = get_title_links(title)
#     type = "shared " + x1

# elif title.text.find(" at ") != -1 or title.text.find(" in ") != -1:
#     if title.text.find(" at ") != -1:
#         x1, link = get_title_links(title)
#         type = "check in"
#     elif title.text.find(" in ") != 1:
#         status = get_div_links(x, "a").text

# elif title.text.find(" added ") != -1 and title.text.find("photo") != -1:
#     type = "added photo"
#     link = get_div_links(x, "a").get_attribute('href')

# elif title.text.find(" added ") != -1 and title.text.find("video") != -1:
#     type = "added video"
#     link = get_div_links(x, "a").get_attribute('href')

# else:
#     type = "others"
##

# def timeline_layout_posts(driver):
#     elementPosts = driver.find_elements_by_xpath('//div[@class="_5pcb _4b0l _2q8l"]')
#     arrayPosts = extract_posts(elementPosts)
#     print('arrayPosts', arrayPosts)
#     return arrayPosts


# def normal_layout_posts(driver):
#     elementPosts = driver.find_elements_by_xpath('//div[@class="_4-u2 _4-u8"]')
#     return
