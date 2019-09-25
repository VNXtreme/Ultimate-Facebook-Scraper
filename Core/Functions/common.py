def reaction_string_to_number(text: str):
    multiplier = 1
    stringNumber = text.split(' ')[0].replace(',', '').replace('.', '')
    hasK = stringNumber.find('K')

    if(hasK != -1):
        stringNumber = stringNumber.replace('K', '')
        multiplier = 1000

    result = int(stringNumber) * multiplier

    return result


def is_timeline_layout(driver):
    try:
        driver.find_element_by_class_name('timelineLayout')
        return True
    except:
        return False
