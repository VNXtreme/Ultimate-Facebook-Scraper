def extract_fb_username(url):
    return url.split("/")[-1]


def extract_follower_number(text):
    followerNumber = text.split(' ', 1)[0].replace(',', '')
    return followerNumber

def convert_string_to_number(text):
    numberInString = text.split(' ')[0]
    if numberInString.find('K'):
        numberInString.replace('.', '').replace(',', '') 
        numberInString = numberInString * 1000
    return numberInString

def is_timeline_layout(driver):
    try:
        driver.find_element_by_class_name('timelineLayout')
        return True
    except:
        return False
