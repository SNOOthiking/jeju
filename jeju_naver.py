# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 09:16:34 2022

@author: medici
"""
import pandas as pd
import numpy as np
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re
import requests

import time
import webdriver_manager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
options = wb.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정 # 코랩은 크롬창을 새로 안띄워준다.
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
url = 'https://map.naver.com/'
a=2939
df_jeju = pd.read_csv('G:/내 드라이브/jeju/df_jeju_naver.csv')
df_jeju.iloc[1831]

while(a<15901):        
    
    driver = wb.Chrome(ChromeDriverManager().install(),options=options)
    driver.get(url)
    
    for i in range(a-1,a+299):
        print(i)
        road = ''.join(df_jeju.iloc[i]['도로명전체주소'].split(' ')[1:3])
        name = df_jeju.iloc[i]['사업장명']
        
        driver.find_element(by=By.CLASS_NAME,value="input_search").clear() # 검색창 초기화 
        driver.find_element(by=By.CLASS_NAME,value="input_search").send_keys(f'{name} {road}') # 상호명 검색 이 부분이 계속 바뀜.
        driver.find_element(by=By.CLASS_NAME,value="input_search").send_keys(Keys.ENTER) # 엔터누르기 
        time.sleep(2.5)
        html = driver.current_url # 검색한 상호명 주소 따오기 
        try:
            res_code = re.findall(r"place/(\d+)", html)[0]
            if res_code != '':
                try:
                    final_url = 'https://pcmap.place.naver.com/restaurant/'+res_code
                    res =requests.get(final_url)   
                    res.encoding='utf-8'
                    html_str = res.text
                    soup = bs(html_str,'html.parser')
                    try:
                        stars = soup.select_one('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz > span._1Y6hi._1A8_M > em').text
                        reviews = soup.select_one('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz > span:nth-child(2) > a > em').text
                    except:
                        stars=0
                        reviews =0
                    df_jeju['n_stars'][i]=stars
                    df_jeju['n_reviews'][i]=reviews
                except:
                    pass
            else:
                df_jeju['n_stars'][i]=0
                df_jeju['n_reviews'][i]=0
            print(res_code)
            print(i,df_jeju.iloc[i])
        except:
            pass
    df_jeju.to_csv('G:/내 드라이브/jeju/df_jeju_naver.csv')
    a+=299
