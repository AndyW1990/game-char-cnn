import os
import time
import requests
import urllib.request
from bs4 import BeautifulSoup
from string import ascii_lowercase as alc
from PIL import Image
from app.params import *

import numpy as np
import pandas as pd

### HELPER FUNCTIONS ###
def get_chars_from_alpha(url, list_query, c):
    response = requests.get(url + list_query + c)
    soup = BeautifulSoup(response.text, 'html.parser')
    char_blocks = soup.find_all(class_="category-page__member")
    return char_blocks

def get_char(char_block):
    char_dir = char_block.find('a').attrs['href']
    char_name = char_block.find('a').attrs['title'].replace('Category:', '')
    invalid = '<>:"/\|?*'
    for char in invalid:
        char_name = char_name.replace(char, '')
    return char_name, char_dir

def get_char_img(char_soup):
    try:
        img_url = char_soup.find(class_="wikia-infobox").find(class_="image").attrs['href']
        img_ext = char_soup.find(class_="wikia-infobox").find('img').get('data-image-name').split('.')[-1]
        image_fname = f'{char_name}.{img_ext}'
        if not os.path.isfile(f'data/images/{image_fname}'):
            urllib.request.urlretrieve(img_url, f'data/images/{image_fname}')   
        img_w, img_h = Image.open(f'data/images/{image_fname}').size
    except:
        img_url, image_fname, img_h, img_w = np.nan, np.nan, np.nan, np.nan     
    return image_fname, img_h, img_w, img_url

def get_char_alignment(char_soup):
    try:
        for i,th in enumerate(char_soup.find(class_="wikia-infobox").find_all('th')):
            if th.find('a'):
                idx = i
                char_alignment = char_soup.find(class_="wikia-infobox").find_all('td')[idx].contents[0].strip('\n')
    except:
        char_alignment = np.nan
    return char_alignment



### MAIN LOOP ###

columns = ['Name', 'URL', 'Image fName', 'Image Height', 'Image Width', 'Image URL', 'Alignment']

url = "https://characterprofile.fandom.com"
list_query = "/wiki/Category:Video_Game_Characters?from="
#breakpoint()
try:
    df = pd.read_csv('data/game_chars.csv')
    df = df[columns]
    l = df['Name'].iloc[-1][0].lower()
    alc = alc[alc.find(l):]
except:
    df = pd.DataFrame(columns=columns)



for c in alc:
    accumulator = []
    
    char_blocks = get_chars_from_alpha(url, list_query, c)
    
    for char_block in char_blocks:
        char_dict = dict.fromkeys(columns)
        char_name, char_dir = get_char(char_block)  
        char_dict['Name'] = char_name
        char_dict['URL'] = url+char_dir
        
        if char_name in df['Name'].tolist():
            print(f'Skipping {char_name}, already downloaded.')
        else:
            char_response = requests.get(url + char_dir)
            char_soup = BeautifulSoup(char_response.text, 'html.parser')
            print(f'Parsing {char_name}...')
        
            char_dict['Image fName'], char_dict['Image Height'], \
            char_dict['Image Width'], char_dict['Image URL'] = get_char_img(char_soup)   
             
            char_dict['Alignment'] = get_char_alignment(char_soup)
            
            accumulator.append(char_dict)
            time.sleep(SLEEP_TIMER)

    df_acc = pd.DataFrame(accumulator)   
    df = pd.concat((df,df_acc))
    df.reset_index(drop=True, inplace = True)
    df.to_csv('data/game_chars.csv', index=False)
            
        

        

        
                        
                    