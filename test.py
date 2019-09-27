likes = '0'
loves = '853 Yêu thích'

def reaction_string_to_number(text: str):
    multiplier = 1
    stringNumber = text.split(' ')[0].replace(',', '').replace('.', '')
    
    hasK = stringNumber.find('K')
    if(hasK != -1):
        stringNumber = stringNumber.replace('K', '')
        multiplier = 1000

    result = int(stringNumber) * multiplier
    
    return result

reaction_string_to_number(likes)
