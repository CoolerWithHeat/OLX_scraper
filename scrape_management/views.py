from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import sent_apartments
import json

last_alert_catergory = None

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
    bot_token = ''
    chat_id = ""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    something_afterwards = callable(doAfter)
    true_announcement = 'https://olx.uz/d/obyavlenie/' in data_tobe_sent
    response = requests.post(url, data=craftMessageHeader(data_tobe_sent, chat_id, something_afterwards))
    if response.status_code == 200 and something_afterwards: doAfter()
    if response.status_code == 200 and true_announcement: 
        sent_apartments.objects.create(apartment_url=data_tobe_sent)

def processResult(each_url):
    full_url = f'https://olx.uz{each_url}'
    previously_checked = sent_apartments.check_if_sent(full_url)
    result = full_url if not previously_checked else None
    return result

class AlertRequest(APIView):
    def post(self, request, *args, **kwargs):
        data = request.body
        data = json.loads(data) if data else None
        if data:
            searchResults = data.get('results')
            keyword = data.get('keyword')  
            district = data.get('district')
            processedResults = list(map(processResult, searchResults))
            filteredResults = [x for x in processedResults if x is not None]
            if len(filteredResults):
                global last_alert_catergory
                alert_category = f'{f'District {district}' if district else ''}{f' With Keyword: {keyword}' if keyword else ''}'
                header_text = getCategoryHeader(alert_category)
                category_changed = not (header_text == last_alert_catergory)
                print(len(searchResults))
                def changeLastCateg():
                    global last_alert_catergory
                    last_alert_catergory = alert_category
                if category_changed:
                    sendTenant(header_text, changeLastCateg)
                for each in filteredResults:
                    sendTenant(each, None)
        return Response({"message": "Alerted Tenant!"}, status=status.HTTP_200_OK)

class AlertClientError(APIView):
    def post(self, request, *args, **kwargs):
        sendTenant('client watchdog experienced failure', None)
        return Response({"message": "Alerted Developer!"}, status=status.HTTP_200_OK)