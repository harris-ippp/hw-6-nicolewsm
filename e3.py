#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

elections = {}
for line in open("ELECTION_ID.txt"):
    line = line.strip().split(" ")
    elections[line[0]] = line[1]

df_combined = []
for year in elections:
    filename = "president_general_" + year + ".csv"

    header = pd.read_csv(filename, nrows = 1).dropna(axis = 1)

    d = header.iloc[0].to_dict()

    df = pd.read_csv(filename, index_col = 0, thousands = ",", skiprows = [1])
    df.rename(inplace = True, columns = d) # rename to democrat/republican
    df.dropna(inplace = True, axis = 1)    # drop empty columns
    df["Year"] = pd.to_datetime(year)
    df["Year"] = df["Year"].dt.year
    df = df[["Democratic", "Republican", "Total Votes Cast", "Year"]].reset_index()
    df_combined.append(df)

df_concat = pd.concat(df_combined)
df_concat["Republican Share"] = df_concat["Republican"] / df_concat["Total Votes Cast"]

df_final=df_concat[['County/City', 'Year', 'Republican Share']]


import matplotlib.pyplot as plt

q3 = ['Accomack County', 'Albemarle County', 'Alexandria City', 'Alleghany County']

for county in q3:
    name = county.lower().replace(" ", "_")  #To generate filename for savefig
    row = df_final[df_final['County/City'].str.contains(county)]
    finalrows = row.groupby(row['Year'], as_index = True).mean()  # to account for counties with (CD X)
    ax = finalrows.plot(kind = 'line', marker = 'o', xticks = finalrows.index)
    ax.grid(ls = 'dotted', color = '0.8')
    plt.xticks(rotation=70)
    plt.yticks(np.arange(0.1, 0.81, 0.1))
    plt.title('Republican Share of Votes in ' + county)
    plt.autoscale()
    plt.tight_layout()

    plt.xlabel('Year of Presidential Election')
    plt.ylabel('Share of Votes')
    plt.savefig(name+'.pdf')
