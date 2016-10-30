"""
Get schedule for Hoy No Circula by iterating through days in a given period and scraping relevant page from www.hoy-no-circula.com.mx.

Specifically focus on identifying dates where restrictions applied to 00 holograms.
"""

import urllib
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from random import choice
import json
import logging
import time

logging.basicConfig(filename='out.log', level=logging.DEBUG)

years = [2015, 2016]
days31 = [i for i in range(1, 32)]
days30 = [i for i in range(1, 31)]
# months = ['marzo', 'abril', 'mayo', 'junio', 'julio']
months = ['enero', 'febrero']

month_days = {'marzo': days31, 'abril': days30, 'mayo': days31, 'junio': days30, 'julio': days31, 'enero': days31, 'febrero': days30}

base_url = 'http://www.hoy-no-circula.com.mx/calendario/'

HEADERS = [
    {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'},
    {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'},
    {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'},
    {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
]

output = {}

for y in years:
    for m in months:
        for d in month_days[m]:
            date = "{}-{}-{}".format(d, m, y)
            logging.info(date)
            url = base_url + date
            headers = choice(HEADERS)
            try:
                page = Request(url, headers=headers)
                soup = BeautifulSoup(urlopen(page).read(), "lxml")
                table = soup.find('table', {'class': 'nc-info'})
                if table:
                    rows = table.findAll('tr')
                    for r in rows:
                        cells = r.findAll('td')
                        if "Holograma 00" in cells[0].get_text():
                            output[date] = cells[1].get_text()
            except urllib.error.HTTPError as e:
                logging.error(e, url)
            except urllib.error.URLError as e:
                logging.error(e, url)
            # time.sleep(choice((0, 1, 2)))

with open("hoy_no_circula_2.json", "w") as f:
    json.dump(output, f)