import requests, re, random, time, os, json
from bs4 import BeautifulSoup

server_host = 'http://localhost:8000'
acceptance_path = '/AlertTentant/'

def manage_data(url):
    db_file = "database.json"
    if not os.path.exists(db_file):
        with open(db_file, "w") as file:
            json.dump({"urls": []}, file)
    with open(db_file, "r") as file:
        data = json.load(file)
    if url in data["urls"]:
        return None
    else:
        data["urls"].append(url)
        with open(db_file, "w") as file:
            json.dump(data, file, indent=4)
    return url

def sendServer(data):
    if data:
        url = server_host + acceptance_path
        requests.post(url, json=data)

def getWaitTime(): return random.uniform(7, 20)

def getSquareMeter(data):
    try: 
        square_number = int(data)
        return square_number if square_number > 30 else None
    except: return None

def getResultCount(soup_data):
    try:
        total_count_span = soup_data.find('span', {'data-testid': 'total-count'})
        if total_count_span:
            text = total_count_span.text.strip()
            number = re.search(r'\d+', text).group()
            return int(number)
        else: return 0
    except: return 0

search_data = [
    {
        'url': 'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/q-%D0%90%D0%B9%D0%B1%D0%B5%D0%BA/?currency=UZS&search%5Bfilter_float_price:from%5D=1500000&search%5Bfilter_float_price:to%5D=2200000',
        'district': None,
        'keyword': 'Айбек',
    },
    {
        'url': 'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/q-oybek/?currency=UZS&search%5Bfilter_float_price:from%5D=1500000&search%5Bfilter_float_price:to%5D=2200000',
        'district': None,
        'keyword': 'oybek',
    },
    {
        'url': 'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/q-%D0%9A%D0%BE%D1%81%D0%BC%D0%BE%D0%BD%D0%B0%D0%B2%D1%82%D1%8B/?currency=UZS&search%5Bfilter_float_price:from%5D=1500000&search%5Bfilter_float_price:to%5D=2200000',
        'district': None,
        'keyword': 'Космонавты',
    },
    {
        'url': 'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/q-kosmonavt/?currency=UZS&search%5Bfilter_float_price:from%5D=1500000&search%5Bfilter_float_price:to%5D=2200000',
        'district': None,
        'keyword': 'kosmonavt',
    },
    {
        'url': 'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/?search%5Bdistrict_id%5D=13&search%5Bfilter_float_price:from%5D=1500000&search%5Bfilter_float_price:to%5D=2200000&currency=UZS',
        'district': 'Mirabad',
        'keyword': None,
    },
    {
        'url': 'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/?search%5Bdistrict_id%5D=24&search%5Bfilter_float_price:from%5D=1500000&search%5Bfilter_float_price:to%5D=2200000&currency=UZS',
        'district': 'Shayxontoxur',
        'keyword': None,
    },
]

def filterResults(data):
    if data:
        return data

while True:
    for each_search_param in search_data:
        url = each_search_param.get('url')
        district = each_search_param.get('district')
        search_keyword = each_search_param.get('keyword')
        results = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        resultsFound = getResultCount(soup)
        if resultsFound:
            cards = soup.find_all('div', class_='css-l9drzq', limit=resultsFound)
            for card in cards:
                anchor = card.find('a', class_='css-qo0cxu')
                number_span = card.find('span', class_='css-1cd0guq')
                apartment_url = None
                apartment_size = None
                if number_span:
                    apartment_size = getSquareMeter(number_span.text.strip()) or None
                else:
                    apartment_size = None

                if anchor and 'href' in anchor.attrs:
                    apartment_url = anchor['href']
                    apartment_url = manage_data(apartment_url)
                else:
                    apartment_url = None
                if apartment_size and apartment_url:
                    try: 
                        if int(apartment_size) > 30: results.append(apartment_url)
                    except: print('apartment size part failed to provide')
        if results and len(results):
            try:
                data = {'results': results, 'keyword': search_keyword, 'district': district}
                sendServer(data)
            except: pass
        else:pass
        print(results)
        print(f'{len(results)} results')
        next_request_time = getWaitTime()
        time.sleep(next_request_time)