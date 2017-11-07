#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs

elections = {}
for line in open("ELECTION_ID.txt"):
    line = line.strip().split(" ")
    elections[line[0]] = line[1]


for year in elections:
    filename = "president_general_" + year + ".csv"
    url = "http://historical.elections.virginia.gov/elections/download/" + elections[year] + "/precincts_include:0/"
    download = requests.get(url)
    with open(filename, "w") as out:
      out.write(download.text)
