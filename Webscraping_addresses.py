#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import sys
from typing import Optional
import pandas as pd
import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# In[2]:


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}


# In[3]:


url = "https://www.gelbeseiten.de/AjaxSuche"
req = requests.get(url, headers= header)
soup = BeautifulSoup(req.content, 'html.parser')


# In[4]:


def post_ajax_search(was: str, wo: str, pos: int):
    req = requests.post("https://www.gelbeseiten.de/AjaxSuche", data={
        'umkreis': -1, 'WAS': was, 'WO': wo, 'position': pos, 'sortierung': 'relevanz'})
    r = req.json()
    return [r[key] for key in ("gesamtanzahlTreffer", "html", "anzahlTreffer")]


# In[5]:


def parse_html(html: str) -> list:
    soup = BeautifulSoup(html, "lxml")
    return [i.text for i in soup.find_all("h2", {"data-wipe-name": "Titel"})]


# In[6]:


def parser(was: str, wo: str) -> list:
    total_treffer, html, parsed_treffer = post_ajax_search(was, wo, 0)
    all_names = parse_html(html)
    i = 0
    while parsed_treffer < total_treffer:
        _, html, treffer = post_ajax_search(was, wo, 51 + i)
        all_names += parse_html(html)
        parsed_treffer += treffer
        i += 10
    return all_names


# In[ ]:





# In[7]:


business_names = parser("Physiotherapie praxis", "rostock")


# In[ ]:





# In[8]:


def parse_html_address(html: str) -> list:
    soup = BeautifulSoup(html, "lxml")
    return [i for i in soup.find_all('address', class_="mod mod-AdresseKompakt")]


# In[9]:


def parser_address(was: str, wo: str) -> list:
    total_treffer, html, parsed_treffer = post_ajax_search(was, wo, 0)
    all_names = parse_html_address(html)
    i = 0
    while parsed_treffer < total_treffer:
        _, html, treffer = post_ajax_search(was, wo, 51 + i)
        all_names += parse_html_address(html)
        parsed_treffer += treffer
        i += 10
    return all_names


# In[10]:


business_addresses = parser_address("Physiotherapie praxis", "rostock")


# In[ ]:





# In[11]:


streets = []
plzs = []
cities = []
tel_nrs = []
places = []



for name in business_addresses:
    ent = name.find('span',class_="mod-AdresseKompakt__entfernung")
    if not "None" in str(type(ent)):
        ent.clear()
    item1 = name.get_text().strip().replace('\t', '')
    item2 = item1.strip().replace('\n', '')
    if len(item2.split(',')) > 1:
        address_only = item2.split(',')[0]
        item2 = item2.split(',')[1]
    else:
        address_only = "No address found"
    plz_mix = item2.split(')')[0]
    if len(item2.split(')'))>1:
        tel = item2.split(')')[1].strip().replace(' ', '')

    else:
        tel=""
    item2 = plz_mix
    if len(item2.split('('))>1:
        place_only = item2.split('(')[1]
    else:
        place_only=""
    item2 = item2.split('(')[0]
    plz = re.split(r'([A-Za-z]+)', item2)[0]


    streets.append(address_only)
    plzs.append(plz)
    tel_nrs.append(tel)
    places.append(place_only)
    


# In[12]:


file1 = open('myfile.csv', 'w', encoding='utf-8')

df = pd.DataFrame({"name":business_names, "street":streets, "plz":plzs, "place":places, "telephone":tel_nrs})
file1.close()


df.to_csv (r'D:\Mastersstudiengang\coding\myfile.csv', index = False, header=True)


# In[ ]:




