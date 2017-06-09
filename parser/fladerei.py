import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import config

name = "Fladerei"

fetch_url = "https://www.fladerei.com/dyn_inhalte/berggasse/tagesfladen_berggasse.html"


def fetch_recourse():
    if config.DEBUG:
        from website import fladerei_html as html
    else:
        r = requests.get(fetch_url)
        r.encoding = "utf-8"  # force UTF-8 as the meta tag is invalid
        html = r.text
    return html


def get_menus():
    soup = BeautifulSoup(fetch_recourse(), 'html.parser')
    table = soup.find("table", {"title": "Tagesfladen"})
    tagesfladen = []
    for smallblue in table.findAll("smallblue"):
        smallblue.extract()

    trs = table.findAll("tr")

    i = 0
    while i < len(trs):
        dateregex = re.compile(r"\d{2}\.\d{2}\.")
        datestring = dateregex.search(trs[i].td.span.text).group(0)
        descr = trs[i]('td')[-1].text.strip()
        extradescr = trs[i + 1]('td')[-1].text.strip()
        if extradescr:
            descr += " " + extradescr
        date = datetime.strptime(datestring, "%d.%m.").replace(year=datetime.today().year)
        tagesflade = {
            "date": date.isoformat(),
            "name": descr
        }
        tagesfladen.append(tagesflade)
        i += 2

    return tagesfladen
