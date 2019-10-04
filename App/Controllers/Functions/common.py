def reaction_string_to_number(text: str) -> int:
    multiplier = 1
    try:
        stringNumber = text.split(' ')[0].replace(',', '.')
        hasK = stringNumber.find('K')

        if(hasK != -1):
            stringNumber = stringNumber.replace('K', '')
            multiplier = 1000

        result = float(stringNumber) * multiplier
    except:
        result = 0

    return result


def is_timeline_layout(driver):
    try:
        driver.find_element_by_class_name('timelineLayout')
        return True
    except:
        return False


def safely_generate_url(fbUrl: str, destination: str) -> str:
    destination = destination if fbUrl[len(
        fbUrl)-1] == '/' else f"/{destination}"
    return fbUrl + destination
