#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup as bs

resp = requests.get("http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2016/office_id:1/stage:General")

soup = bs(resp.content, "html.parser")

rows = soup.find_all("tr", "election_item")

#saving it as txt file, so that we don't have to send the site a requests
#when we are doing parts 2 and 3.
with open("ELECTION_ID.txt", "w") as output:
    x = 0
    for tag in rows:
        year = [tag.contents[1].contents[0] for tag in rows][x]
        fullid = tag.get('id')
        idonly = fullid.split('-')[2]
        x += 1
        output.write(year + " " + idonly + '\n')
