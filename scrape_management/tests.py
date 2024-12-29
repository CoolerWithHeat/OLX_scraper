from django.test import TestCase
import requests

def getStars(amount):
    stars = ''
    for x in range(amount):
        stars+='🌟'
    return stars

def getCategoryHeader(text):
    each_side_stars = 3 if len(text) > 20 else 4
    if len(text) >= 24: each_side_stars = 2
    stars = getStars(each_side_stars)
    return f"{stars} *{text}* {stars}"

def craftMessageHeader(data, chat_id, special=False):
    header = {
        'chat_id': chat_id,
        'text': data,
    }
    if special: header['parse_mode'] = 'MarkdownV2'
    return header

def sendTenant(data_tobe_sent, doAfter=None):
    import requests
    bot_token = '7370703241:AAEjQOXbSlRW4m5Pm1OXKHf18x35ejuLc78'
    chat_id = "6375161482"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    something_afterwards = callable(doAfter)
    true_announcement = 'https://olx.uz/d/obyavlenie/' in data_tobe_sent
    response = requests.post(url, data=craftMessageHeader(data_tobe_sent, chat_id, something_afterwards))
    if response.status_code == 200 and something_afterwards: doAfter()

header = getCategoryHeader('With Keyword: Космонавты')
sendTenant(header)