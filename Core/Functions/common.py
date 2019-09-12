def extract_fb_username(url):
    return url.split("/")[-1]


def extract_follower_number(text):
    followerNumber = text.split(' ', 1)[0].replace(',', '')
    return followerNumber
