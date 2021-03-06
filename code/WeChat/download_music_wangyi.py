# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 01:51:57 2018

@author: Administrator
"""

import requests, re, json, os, urllib, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np

def get_html(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com'
            }
    try:
        response = requests.get(url, headers = headers)
        html = response.text
        return html
    except:
        print('error')
        pass

def download_chrome_driver(url, sleep = 'n'):
    chrome_options = Options()
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #chrome_options.add_experimental_option("prefs", prefs)
    #chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('-headless')
    chrome_options.add_argument('-disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    if sleep == 'y':
        time.sleep(np.random.randint(1,5,1))
    return driver
    
def get_song_id_by_name(song_name):
    song_url = 'https://music.163.com/#/search/m/?s={}&type=1'.format(song_name)
    driver = download_chrome_driver(song_url)
    iframe = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe)   
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    song_id = soup.find(class_ = 'text').find('a').get('href').split('=')[-1]
    song_nam = soup.find(class_ = 'text').text
    driver.quit()
    return (song_nam, song_id)
    
    
def get_singer_info(soup):
    
    links = soup.find('ul', class_='f-hide').find_all('a')
    song_IDs =[]
    song_names = []
    for link in links:
        song_ID = link.get('href').split('=')[-1]
        song_name = link.get_text()
        song_IDs.append(song_ID)
        song_names.append(song_name)
    return zip(song_names, song_IDs)

        
def download_song(song_name, song_id):
    singer_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)
    print('正在下载歌曲:{}'.format(song_name))
    urllib.request.urlretrieve(singer_url, path + '\\{}.mp3'.format(song_name))
    
if __name__== '__main__':
    singer_id = input('Singer\'s ID:')
    #singer_name = input('歌手姓名：')
 
    start_url = 'http://music.163.com/artist?id={}'.format(singer_id)
    html = get_html(start_url)
    soup = BeautifulSoup(html, 'lxml')
    singer_name = soup.find(id = 'artist-name').text
    singer_infos = get_singer_info(soup)

    path = 'F:\\KuGou\\{}'.format(singer_name)
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
    print('开始下载 %s 的歌曲...' % singer_name)
    for singer_info in singer_infos:
        
        download_song(singer_info[0].split('/')[-1], singer_info[1])
