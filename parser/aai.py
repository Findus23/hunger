import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

import config

name = "AAI"

fetch_url = "http://www.aai-wien.at/aai-mensa"

dateregex = re.compile("plan (\d{2}\.\d{2}\.)")


def fetch_recourse():
    if config.DEBUG:
        from website import aai_html as html
    else:
        r = requests.get(fetch_url)
        html = r.text
    return html


def get_menus():
    tagesmenus = []
    html = fetch_recourse()
    startdatestring = dateregex.search(html).groups()[0]
    startdate = datetime.strptime(startdatestring, "%d.%m.").replace(year=datetime.today().year)
    print(startdate)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"class": "mitrand", "border": "1", "align": "center"})
    i = 0
    for tr in table.tbody.findAll("tr"):
        menutype = tr.td.text.strip()
        if not menutype:
            continue
        for td in tr.findAll("td")[1:]:
            tagesmenu = {
                "type": menutype,
                "name": td.text.split("(")[0].strip(),
                "date": startdate + timedelta(days=i)
            }
            tagesmenus.append(tagesmenu)
        i += 1
    return tagesmenus


if __name__ == '__main__':
    print(get_menus())
