from bs4 import BeautifulSoup
from lxml import html
import requests
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import csv
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
header={"accept-encoding": "gzip, deflate"}
req=requests.get('https://web.archive.org/web/20241213143621/https://www.billboard.com/charts/year-end/2024/billboard-global-200/')
scr=(req.text)
chart=[]
soup=BeautifulSoup(scr,'lxml')
items = soup.find_all('li', {'class': 'o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 lrv-u-border-color-grey-light lrv-u-padding-l-2 lrv-u-padding-l-1@mobile-max'})
for item in items:
    song = item.find('h3', {'class': 'c-title a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max'})
    artist = item.find('span', {'class': 'c-label a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block'})
    if artist or song:
        chart.append({'pos':len(chart)+2,'artist': artist.text.strip(),
                  'song': song.text.strip()})
chart.insert(0, {'pos': 1,'artist': 'Benson Boone', 'song': 'Beautiful Things'})
for entry in chart:
    entry['artist']=entry['artist'].replace(' &', ',')
    entry['artist']=entry['artist'].replace(' X', ',')
    entry['artist']=entry['artist'].replace(' x', ',')
    entry['artist']=entry['artist'].replace(' Featuring', ',')
    entry['artist']=entry['artist'].replace(' vs.', ',')
for entry in chart:
    browser = wd.Chrome()
    browser.get('https://www.shazam.com/')
    open_search = browser.find_element("class name", 'Search_icon__Poc_G')
    open_search.click()
    search = browser.find_element("class name", "Search_input__HkJTl")
    search.send_keys(f'{entry["artist"]} {entry["song"]}')
    time.sleep(1)
    search.click()
    search.send_keys(Keys.ENTER)
    time.sleep(2)
    soup_1 = BeautifulSoup(browser.page_source, 'lxml')
    items=[]
    people = soup_1.find_all('div', {'class': 'SongCredits_people__pHGX5'})
    categories = soup_1.find_all('span', {'class': 'Text-module_text-gray-900__Qcj0F Text-module_fontFamily__cQFwR Text-post-module_size-base__o144k Text-module_fontWeightBold__4NHce'})
    if len(people) == len(categories):
        for i in range(len(people)):
            people[i]=people[i].find_all('div', {'class': 'Text-module_text-black-200__8cY0O Text-module_fontFamily__cQFwR SongCredits_name__3ItNW Text-post-module_size-base__o144k Text-module_fontWeightNormal__kB6Wg Text-module_textOverflowEllipsis__J7BCo'})
            for j in range(len(people[i])):
                people[i][j]=people[i][j].text.strip()
            items.append([categories[i], people[i]])
    time.sleep(1)
    if soup_1.find('h3', {'class': 'Text-module_text-white__l-SDK Text-module_fontFamily__cQFwR TrackPageHeader_genreNoUrl__u_v2b Text-post-module_size-base__o144k Text-module_fontWeightNormal__kB6Wg Text-module_headingReset__Mn-tB'}):
        artist=soup_1.find('span', {'class': 'Text-module_text-white__l-SDK Text-module_fontFamily__cQFwR TrackPageHeader_link__q0Id5 Text-post-module_size-md-large__4coGy Text-module_fontWeight500__iJDFU'}).text.strip()
        genre=soup_1.find('h3', {'class': 'Text-module_text-white__l-SDK Text-module_fontFamily__cQFwR TrackPageHeader_genreNoUrl__u_v2b Text-post-module_size-base__o144k Text-module_fontWeightNormal__kB6Wg Text-module_headingReset__Mn-tB'}).text.strip()
    artists=[]
    songwriters=[]
    producers=[]
    credit={'song':entry['song'],'artist': artist,'genre': genre}
    for item in items:
        credit[item[0].text.strip()]=item[1]
    credits.append(credit)
    browser.quit()
adf=pd.DataFrame(credits) #adf - active data frame
pd.DataFrame(credits).to_csv('DATA_raw.csv')
