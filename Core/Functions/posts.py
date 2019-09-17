def scrape_posts(driver, isTimelineLayout: bool):
    if isTimelineLayout:
        elementPosts = driver.find_elements_by_xpath(
            '//div[@class="_5pcb _4b0l _2q8l"]')
        return extract_posts(elementPosts)

    else:
        return normal_layout_posts(driver)

    return 1

# def timeline_layout_posts(driver):
#     elementPosts = driver.find_elements_by_xpath('//div[@class="_5pcb _4b0l _2q8l"]')
#     arrayPosts = extract_posts(elementPosts)
#     print('arrayPosts', arrayPosts)
#     return arrayPosts


def normal_layout_posts(driver):
    elementPosts = driver.find_elements_by_xpath('//div[@class="_4-u2 _4-u8"]')
    return


def get_link(driver) -> str:
    link = driver.find_element_by_tag_name(
        'abbr').find_element_by_xpath(".//ancestor::a")

    if link.get_attribute('ajaxify') is None:
        return link.get_attribute('href')

    return link.get_attribute('ajaxify')


def extract_posts(elements) -> list:
    try:
        posts = []
        for postElement in elements:
            try:
                video_link = " "
                title = " "
                status = " "
                link = ""
                img = " "
                time = " "
                message = post_message(postElement)
                # time
                time = get_time(postElement)
                link = get_link(postElement)

                # title
                title = get_title(postElement)
                if title.find("shared a memory") > 0:
                    postElement = postElement.find_element_by_xpath(
                        ".//div[@class='_1dwg _1w_m']")
                    title = get_title(postElement)

                # if not isinstance(title, str):
                #     title = title.text

                status = get_status(postElement)

                status = status.replace("\n", " ")
                title = title.replace("\n", " ")

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
                posts.append([message, time, title, link, status, reactions])

            except Exception as extractError:
                return 'extract loop: '+extractError
        return posts
    except Exception as e:
        print("Exception (extract_posts)",
              "Status =", e)

    return


def total_like(element) -> str:
    return element.find_element_by_xpath('.//span[@data-testid="UFI2TopReactions/tooltip_LIKE"]/a').get_attribute('aria-label')


def total_love(element) -> str:
    return element.find_element_by_xpath('.//span[@data-testid="UFI2TopReactions/tooltip_LOVE"]/a').get_attribute('aria-label')


def total_haha(element) -> str:
    return element.find_element_by_xpath('.//span[@data-testid="UFI2TopReactions/tooltip_HAHA"]/a').get_attribute('aria-label')


def total_reaction(element) -> str:
    return element.find_element_by_xpath('.//span[@class="_3dlg"]/span/span').text


def total_comment(element) -> str:
    return element.find_element_by_xpath('.//a[@data-testid="UFI2CommentsCount/root"]').text


def total_share(element):
    return element.find_element_by_xpath('.//a[@data-testid="UFI2SharesCount/root"]').text


def post_message(element):
    return element.find_element_by_xpath('.//div[@class="_5pbx userContent _3576"]/p').get_attribute('innerHTML')


def get_status(x):
    status = ""
    try:
        status = x.find_element_by_xpath(".//div[@class='_5wj-']").text
    except:
        try:
            status = x.find_element_by_xpath(
                ".//div[@class='userContent']").text
        except:
            pass
    return status


def get_div_links(x, tag):
    try:
        temp = x.find_element_by_xpath(".//div[@class='_3x-2']")
        return temp.find_element_by_tag_name(tag)
    except:
        return ""


def get_title_links(title):
    l = title.find_elements_by_tag_name('a')
    return l[-1].text, l[-1].get_attribute('href')


def get_title(x):
    title = ""
    try:
        title = x.find_element_by_xpath(".//span[@class='fwb fcg']/a")
    except:
        try:
            title = x.find_element_by_xpath(".//span[@class='fcg']/a")
        except:
            try:
                title = x.find_element_by_xpath(".//span[@class='fwn fcg']/a")
            except:
                pass
    finally:
        return title.text


def get_time(x):
    time = ""
    try:
        time = x.find_element_by_tag_name('abbr').get_attribute('title')
        time = str("%02d" % int(time.split(", ")[1].split()[1]), ) + "-" + str(
            ("%02d" % (int((list(calendar.month_abbr).index(time.split(", ")[1].split()[0][:3]))),))) + "-" + \
            time.split()[3] + " " + str("%02d" % int(time.split()[5].split(":")[0])) + ":" + str(
            time.split()[5].split(":")[1])
    except:
        pass

    finally:
        return time


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
