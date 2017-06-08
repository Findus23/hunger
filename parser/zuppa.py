import re
from datetime import datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup

DEBUG = False

name = "Zuppa"

fetch_url = "http://www.zuppa.at/essen/"

dateregex = re.compile("(\d+\.\d+\.\d{4})")


def fetch_recourse():
    if DEBUG:
        from website import zuppa_html as html
    else:
        r = requests.get(fetch_url)
        html = r.text
    return html


def get_menus():
    tagesmenus = []
    soup = BeautifulSoup(fetch_recourse(), 'html.parser')
    hs_div = get_hauptsachen(soup)

    for day_p in hs_div.find_all("p", text=dateregex):
        datestring = dateregex.search(day_p.text).group(0)
        date = datetime.strptime(datestring, "%d.%m.%Y")
        for p in range(2):
            title = []
            p = day_p.findNext("p")
            for strong in p.findAll('strong'):
                if not any(str.isdigit(c) for c in strong.text):
                    title.append(strong.text.strip())
            tagesflade = {
                "date": date.strftime("%Y-%m-%d"),
                "name": " ".join(title).replace("\n", " ")
            }
            day_p = p  # findNext should find the second mea
            tagesmenus.append(tagesflade)
    return tagesmenus

def get_hauptsachen(soup):
    divs = soup.findAll("div", {"class": "menue_box"})
    for div in divs:
        if div.h2.text == "HAUPT SACHEN":
            return div
