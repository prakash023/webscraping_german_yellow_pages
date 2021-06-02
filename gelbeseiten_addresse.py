#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import sys
from typing import Optional
import pandas as pd
import re


# In[2]:


url = 'https://www.gelbeseiten.de/Suche/Physiotherapie%20praxis/Wismar'
print(url)


# In[3]:


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}


# In[4]:


req = requests.get(url, headers= header)
soup = BeautifulSoup(req.content, 'html.parser')


# In[5]:


soup.title


# In[6]:


articles = soup.find_all('p', class_= 'd-inline-block mod-Treffer--besteBranche')

#business_name = soup.find_all( 'articles', h2 ='data-wipe-name="Titel"')
#business_name = soup.find_all('h2', attrs ={"data-wipe-name="Titel"})
#for name in business_name:
#    print(name.get_text())

#print(len(business_name))


# In[7]:


#file2 = open('physio_names.csv', 'w', encoding='utf-8')

#business_name = soup.find_all( 'articles', h2 ='data-wipe-name="Titel"')
names = []

business_name = soup.find_all('h2', attrs ={"data-wipe-name":"Titel"})
for name in business_name[:]:
    
    names.append(name.get_text())


# In[8]:



#physio_names = []
#business_name = soup.find_all('h2')
#for name in business_name:
#    physio_names.append(name.get_text())

#print(h2)

#len(physio_names)


# In[9]:


#physio_address_clean = []
#physio_address = soup.find_all('address')
#physio_address
#for name in physio_address:
   # print("--------------------------------------")
   # print("--------------------------------------")
    #print(name)
   # print("--------------------------------------")
   # print("--------------------------------------")
  #  addr = name.find('address', 'p')
  #  if not "None" in str(type(addr)):
  #      addr.clear()
    #business_name1 = soup.find_all('p', class_="Adresse")
    #business_name1[0].get_text().strip().replace('\t', '')
    #print(business_name1[0].get_text)

#name
    
    
    #item1 = name.get_text().strip().replace('\t', '')
    #item2 = item1.strip().replace('\n', '')
    
#    physio_address_clean.append(addr)
    
#print(str(physio_address_clean))


# Distance and tabs and spaces are removed!!

# In[10]:


#df = pd.DataFrame({"Name":physio_names,"Address":physio_address})


# In[11]:


#physio_address


# In[12]:


len(names)


# In[13]:


#listof Address from Rostok

streets = []
plzs = []
cities = []
tel_nrs = []
places = []

business_name = soup.find_all('address', class_="mod mod-AdresseKompakt")

#file1 = open('myfile.csv', 'w', encoding='utf-8')
for name in business_name:
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
    city = re.split(r'([A-Za-z]+)', item2)[1]


    streets.append(address_only)
    plzs.append(plz)
    cities.append(city)
    tel_nrs.append(tel)
    places.append(place_only)
    #print(address_only + "," + plz + "," + city + "," + tel + "," + place_only + "\n")
       
    
    
#file1.close()

#print(name.get_text())
#print(list(name.get_text()))

#physio_address_clean


# In[ ]:





# In[14]:


#business_name1 = soup.find_all('address', class_="mod mod-AdresseKompakt")
#business_name1[0].get_text().strip().replace('\t', '')


# In[15]:


#business_name = soup.find_all('address')
#for name in business_name:
#    ent = name.find('span',class_="mod-AdresseKompakt__entfernung")
#    if not "None" in str(type(ent)):
#        ent.clear()
#    item1 = name.get_text().strip().replace('\t', '')
#    item2 = item1.strip().replace('\n', '')
#    item2 = item2.split(',')[0]
#    print(item2)


# In[16]:


df = pd.DataFrame({"name":names, "street":streets, "plz":plzs, "place":places, "telephone":tel_nrs})
df


# In[17]:


#df.to_csv(r'D:\Mastersstudiengang\coding\File_Name_new.csv')

