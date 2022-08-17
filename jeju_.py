# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 13:43:59 2022
제주도 로드 맵 
@author: medici
"""
1+1
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests 
import urllib.request
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

jeju_RawDF = pd.read_csv('C:/SEONWOO/jeju/제주음식점.csv',encoding='cp949')

jeju_RawDF.info()

'''
jeju_RawDF.info
Out[492]: 
<bound method DataFrame.info of               사업장명 업종구분대분류  ...  도로명우편번호          데이터갱신일자
0             카페송키   일반음식점  ...  63166.0  2018-12-01 2:20
1      그림책방앤카페노란우산   일반음식점  ...  63062.0  2019-01-27 2:40
2         에릭스에스프레소   일반음식점  ...  63361.0  2018-11-04 2:36
3         일품순두부한림점   일반음식점  ...  63030.0  2019-01-17 2:40
4         팔도실비집아라점   일반음식점  ...  63248.0  2020-09-13 2:40
           ...     ...  ...      ...              ...
42597        커피전문점   휴게음식점  ...      NaN  2020-12-12 2:40
42598      아름다운서귀포   휴게음식점  ...      NaN  2020-11-20 2:40
42599       붕어빵과오뎅   휴게음식점  ...  63640.0  2020-12-04 2:40
42600         인정김밥   휴게음식점  ...  63521.0  2021-05-26 2:40
42601       삼춘네칼국수   휴게음식점  ...  63522.0  2021-04-15 2:40

[42602 rows x 16 columns]>

jeju_RawDF.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 42602 entries, 0 to 42601
Data columns (total 16 columns):
 #   Column   Non-Null Count  Dtype  
---  ------   --------------  -----  
 0   사업장명     42602 non-null  object     ★
 1   업종구분대분류  42602 non-null  object 
 2   업종구분소분류  42599 non-null  object  ★
 3   인허가일자    42602 non-null  int64  
 4   인허가취소일자  0 non-null      float64
 5   영업상태명    42602 non-null  object    
 6   상세영업상태명  42602 non-null  object   ★
 7   폐업일자     23445 non-null  float64
 8   휴업시작일자   0 non-null      float64
 9   휴업종료일자   0 non-null      float64
 10  재개업일자    0 non-null      float64
 11  소재지면적    41998 non-null  object 
 12  소재지전체주소  42425 non-null  object   ★
 13  도로명전체주소  27767 non-null  object   ★
 14  도로명우편번호  27428 non-null  float64
 15  데이터갱신일자  42602 non-null  object   
dtypes: float64(6), int64(1), object(9)
memory usage: 5.2+ MB
''' 
# 필요한 컬럼만 사용
jeju_RawDF1 = jeju_RawDF[['사업장명','업종구분소분류','상세영업상태명','소재지전체주소','도로명전체주소']]
# 폐업 데이터는 필요없으니 영업중인 데이터만 jeju_NewDF로 
jeju_NewDF = jeju_RawDF1[jeju_RawDF1['상세영업상태명']=='영업']

# jeju_NewDF.head() 확인용

# 데이터 임시저장 
jeju_NewDF.to_csv('C:/SEONWOO/jeju/jeju_new.csv',encoding='cp949',index=False)

# 데이터 불러오기 
jeju_NewDF = pd.read_csv('C:/SEONWOO/jeju/jeju_new.csv',encoding='cp949')
# 데이터 nan 확인 
jeju_NewDF.isna().sum()
'''
사업장명         0
업종구분소분류      2
상세영업상태명      0
소재지전체주소     94
도로명전체주소    232

''' # 어떻게 변경할 것인가 확인  업종구분소분류가 NaN = 2건 직접 변경해주기 
jeju_Gita.isna().sum()
jeju_NewDF[jeju_NewDF['업종구분소분류'].isnull()]
'''
           사업장명  ...                                   도로명전체주소
26200     다정한식탁  ...          제주특별자치도 서귀포시 중문로81번길 5, 2층 (중문동)
40851  스타월드 라운지  ...  제주특별자치도 서귀포시 안덕면 녹차분재로 218, 제주항공우주박물관 1층
# 라운지 = 휴게시설 업체가 들어와있지만 어떤 판매행위를 하는지 모르기 때문에 제거 
'''
jeju_NewDF.loc[26200]['업종구분소분류'] = '양식'
jeju_NewDF=jeju_NewDF.drop([40851]) 

# 데이터 NaN 확인 
jeju_NewDF.isna().sum()
'''
사업장명         0
업종구분소분류      0
상세영업상태명      0
소재지전체주소     94
도로명전체주소    232
'''
# 데이터 임시저장 
jeju_NewDF.to_csv('C:/SEONWOO/jeju/jeju_new.csv',encoding='cp949',index=False)
jeju_NewDF = pd.read_csv('C:/SEONWOO/jeju/jeju_new.csv',encoding='cp949')
jeju_Gita = jeju_NewDF[jeju_NewDF['업종구분소분류']=='기타']
jeju_Gita

# 데이터 검색 되는지 확인 

driver = webdriver.Chrome('C:/SEONWOO/chromedriver.exe')

import time
time.sleep(3)

search_loc = jeju_Gita.iloc[0,0]
url = 'https://map.naver.com/'
driver.get(url)
driver.find_element_by_class_name("input_search").clear()
driver.find_element_by_class_name("input_search").send_keys('제주 어린왕자감귤밭')
driver.find_element_by_class_name("input_search").send_keys(Keys.ENTER)
html = driver.current_url

res = requests.get(html)
res.encoding='utf-8'
html_str = res.text
driver.find_element_by_css_selector("_3ocDE").text
driver.find_element_by_class_name('place_on_pcmap')

driver.find_element_by_xpath("//*[@id='app-root']/div/div/div/div[2]/div[1]")
driver.find_element_by_class_name("title")
driver.find_element_by_xpath("//*[@id='_pcmap_list_scroll_container']/ul/li[1]")
cu = driver.current_url # 검색이 성공된 플레이스에 대한 개별 페이지 
res_code = re.findall(r"place/(\d+)", cu) 
final_url = 'https://pcmap.place.naver.com/restaurant/'+res_code[0]+'/review/visitor#' 

res1 =requests.get(final_url)
res1.encoding='utf-8'
html_str = res1.text
soup = BeautifulSoup(html_str,'html.parser')

soup.select_one('#_title > span._3ocDE').text
pars_code =[]
category = []
# 정리 1. 이 방식대로 하면 비슷한 이름 파싱이 안된다. Ex ) 제주 제주우드펍 = 무드우드, 우드스탁 
# 우드라는 이름때문에 3개씩 잡히는데 이 경우 그냥 넘어간다. 

driver = webdriver.Chrome('C:/SEONWOO/chromedriver.exe') # 크롬드라이버로 열기 
time.sleep(2)
url = 'https://map.naver.com/'                          # 네이버 맵 메인화면
driver.get(url)                                            # 크롬드라이버에 올리기
jeju_Gita.head(5)
for i in jeju_Gita.iloc[:,0]:
    name = jeju_Gita.iloc[i]['사업장명']
    driver.find_element_by_class_name("input_search").clear() # 검색창 초기화 
    driver.find_element_by_class_name("input_search").send_keys(f'제주 {name}') # 상호명 검색 이 부분이 계속 바뀜.
    driver.find_element_by_class_name("input_search").send_keys(Keys.ENTER) # 엔터누르기 
    time.sleep(4)
    html = driver.current_url # 검색한 상호명 주소 따오기 
    res_code = re.findall(r"place/(\d+)", html) # place 이후 부분이 
    if res_code ==[]:
        res_code = [0]
        pars_code.append(res_code)
        category.append('0')
    else:
        final_url = 'https://pcmap.place.naver.com/restaurant/'+res_code[0]
        res =requests.get(final_url)
        res.encoding='utf-8'
        html_str = res.text
        soup = BeautifulSoup(html_str,'html.parser')
        pars_code.append(res_code)
        category.append(soup.select_one('#_title > span._3ocDE').text)
category
pars_code
pd.DataFrame(pars_code)

jeju_Gita[jeju_Gita['사업장명']=='제주우드펍']

# 두번째 방법 지도에 상호명 + 주소 로 검색 대충 시~ 동 까지만 검색하니 하나의 자료만 나오는것 같다.
# 찾아 보니 소재지 전체 주소가 없는 기타는 6개로 확인된다. 
# 먼저 작업을 해주도록 하겠다. 

new_juso =np.where(pd.notnull(jeju_NewDF['소재지전체주소'])==True,jeju_NewDF['소재지전체주소'],jeju_NewDF['도로명전체주소'])
jeju_NewDF['소재지전체주소'] = new_juso
jeju_NewDF.isnull().sum()
'''
사업장명         0
업종구분소분류      0
상세영업상태명      0
소재지전체주소      0
도로명전체주소    232
''' 
# 도로명도 똑같이 소재지주소로 바꿔주겠다. 
new_street_juso =np.where(pd.notnull(jeju_NewDF['도로명전체주소'])==True,jeju_NewDF['도로명전체주소'],jeju_NewDF['소재지전체주소'])
jeju_NewDF['도로명전체주소'] = new_street_juso
jeju_NewDF.isnull().sum()

'''
사업장명       0
업종구분소분류    0
상세영업상태명    0
소재지전체주소    0
도로명전체주소    0
'''

driver = webdriver.Chrome('C:/SEONWOO/chromedriver.exe') # 크롬드라이버로 열기 
time.sleep(2)
url = 'https://map.naver.com/'                          # 네이버 맵 메인화면
driver.get(url)                                            # 크롬드라이버에 올리기

pars_code =[]         # 검색했을 때 아예 검색 되지 않는 녀석들 찾아서 지우기 위함(폐업)
category = []         # 카테고리 변경을 위한 리스트 
# 두번째 방법 지도에 상호명 + 주소 로 검색 대충 시~ 동 까지만 검색하니 하나의 자료만 나오는것 같다.
# 동까지 검색했을 때 기존 안나오는 경우가 발생 
time.sleep(2.7)
for i in range(2719,len(jeju_Gita)):
    
    name = jeju_Gita.iloc[i]['사업장명']
    juso = ' '.join(jeju_Gita.iloc[i]['소재지전체주소'].split(' ')[1:3])
    driver.find_element_by_class_name("input_search").clear() # 검색창 초기화 
    driver.find_element_by_class_name("input_search").send_keys(f'{name} {juso}') # 상호명 검색 이 부분이 계속 바뀜.
    driver.find_element_by_class_name("input_search").send_keys(Keys.ENTER) # 엔터누르기 
    time.sleep(2.7)
    html = driver.current_url # 검색한 상호명 주소 따오기 
    res_code = re.findall(r"place/(\d+)", html) # place 이후 부분이 
    if res_code ==[]:
        res_code = [0]
        pars_code.append(res_code)
        category.append('0')
    else:
        final_url = 'https://pcmap.place.naver.com/restaurant/'+res_code[0]
        res =requests.get(final_url)
        res.encoding='utf-8'
        html_str = res.text
        soup = BeautifulSoup(html_str,'html.parser')
        pars_code.append(res_code)
        category.append(soup.select_one('#_title > span._3ocDE').text)
        
# 검색에 문제 발생 같은 지역 = 비슷한 이름 안됨. 
# 본점등 원래 네이버에 설정된 이름과 맞지 않으면 또 안됨 
# 문제가 몇개 안나오면 다이렉트 수정 
# 많이 나오면 알고리즘 수정 
# 안나온거 많으면 지도 말고 네이버 검색창에다 안나온거만 검색하는 방법도 좋을듯 하다 


# 위 포문으로 얻은 업종구분소분류(기타) 2828개중 1303개 (없거나 2개이상 오류)를 제외한 
# 1525개를 먼저 jeju_Gita 데이터 프레임에 집어 넣으려고한다 
# 나머지 1303개는 검색방법을 달리해서 (주소검색 등) 얻으려고 한다. 
# 만들어진 카테고리와 사업자명을 하나의 데이터프레임으로 만든다. 
aaa = pd.DataFrame([np.array(category),jeju_Gita['사업장명']]) 
# 데이터 모양이 가로로 되어있기 때문에 전치해주고
aaa=aaa.T
# 보기 쉬운 컬럼으로 추가해주었다.
aaa.columns =['업종','사업장명']

# 데이터 임시저장 
aaa.to_csv('C:/SEONWOO/jeju/jeju_gita_change.csv')
# 위 알고리즘으로 찾지 못한 데이터들은 0 으로 주었는데 0의 로우가 1303개임을 확인했다.
aaa[aaa['업종']=='0']

jeju_Gita.columns
# 기존 jeju_Gita update 새로운 카테고리로 업데이트 해주는 작업이다.
# 같은값만 확인해서 바꾸려고하면 오류가 발생하기 때문에 인덱스로 접근해 주었다. 
# 인덱스값의 숫자만 얻으려면 index의 tolist()함수로 리스트화해서 [0] 번 즉 자기자신값만 
# inum 이라는 변수로 저장해 두고 
# 로케이션 인덱스로 다이렉트로 들어가서 변경해주었다. 
for i in range(len(aaa)):
    name = aaa['사업장명'][i]
    inum = jeju_Gita[jeju_Gita['사업장명']==name].index.tolist()[0]
    jeju_Gita.loc[inum]['업종구분소분류'] = aaa.loc[i]['업종']
jeju_Gita[['사업장명','업종구분소분류']]
# jeju_Gita 데이터 저장. 다른 곳에서 할 수 있기 때문에 파일화했다. 
jeju_Gita.to_csv('C:/SEONWOO/jeju/jeju_Gita.csv',index=False)

# 이제 읽어서 1303개를 얻는 작업을 해주려고한다. 위 방식과 비슷하지만 
# 두가지를 생각 중이다. 첫번째는 도로명주소로 검색 
# 두번째는 네이버 검색창에 검색 

jeju_Gita = pd.read_csv('C:/SEONWOO/jeju/jeju_Gita.csv')

gita_01 = jeju_Gita[jeju_Gita['업종구분소분류']=='0']

jeju_Gita.loc[2562]['업종구분소분류'] ='카페'
jeju_Gita.loc[2826]['업종구분소분류'] ='카페'
gita_01.iloc[0]
driver = webdriver.Chrome('C:/SEONWOO/chromedriver.exe') # 크롬드라이버로 열기 
time.sleep(2)
url = 'https://map.kakao.com/'                          # 네이버 맵 메인화면
driver.get(url)                                            # 크롬드라이버에 올리기
jeju_Gita
jeju_Gita.iloc[0:5,0:2]
time.sleep(2.7)
# 다음 카카오맵으로 재검색
for i in range(0,len(gita_01)):
    
    road = ''.join(gita_01.iloc[i]['도로명전체주소'].split(' ')[1:3])
    name = gita_01.iloc[i]['사업장명']
    driver.find_element_by_id('search.keyword.query').clear() # 검색창 초기화 
    driver.find_element_by_id("search.keyword.query").send_keys(f'{road} {name} ') # 상호명 검색 이 부분이 계속 바뀜.
    driver.find_element_by_id("search.keyword.query").send_keys(Keys.ENTER) # 엔터누르기 
    time.sleep(2.7)
    if driver.find_element_by_class_name('noResultDesc').text == '검색어의 철자가 정확한지 다시 한번 확인해 주세요.\n장소를 찾을 때 전화번호, 주소도 활용해 보세요.':
        pass
    elif driver.find_element_by_class_name('addrtitle').text == '주소':
        pass
    else:
        category = driver.find_element_by_class_name('subcategory').text
        num = gita_01.iloc[i].name
        print(name,category)
        jeju_Gita.loc[num]['업종구분소분류'] = category
# 1302 개에서 570 개 남음 폐업 가능성 있음  하나씩 찾아서 넣기보다는 그냥 삭제하는게 효과적 

jeju_Final_df = jeju_NewDF[jeju_NewDF['업종구분소분류'] != '0']
jeju_NewDF.columns
jeju_NewDF['업종구분소분류']
jeju_NewDF 
jeju_Gita
jeju_NewDF
for i in range(len(jeju_NewDF)):
    name_01 = jeju_NewDF.loc[i]['사업장명'] 
    if len(jeju_Gita[jeju_Gita['사업장명'] == name_01]) == 0:
        pass 
    else :
        cate_01 = jeju_Gita[jeju_Gita['사업장명']==name_01]['업종구분소분류']
        
        jeju_NewDF.loc[i]['업종구분소분류'] =cate_01.iloc[0]
        
jeju_Final_df.to_csv('C:/SEONWOO/jeju/jeju_final.csv',encoding='cp949',index=False)

len(jeju_Final_df['업종구분소분류'].unique())
jeju_Final_df['업종구분소분류'].unique()
# 카페 / 한식 / 육류,고기요리 / 양식 / 중식 / 일식 / 치킨 / 분식 / 주점 / 야식 / 
'''
([['브런치', '테마카페', '카페,디저트', '한식', '양식', '정종/대포집/소주방', '맥주,호프',
       '호프,요리주점', '분식', '육류,고기요리', '식육(숯불구이)', '중국식', '돼지고기구이', '일식',
       '공방', '돈가스', '경양식', '떡볶이', '중화요리', '갈비', '해물,생선요리', '실내포장마차',
       '호프/통닭', '카페', '이탈리아음식', '펜션', '커피전문점', '게스트하우스', '패밀리레스트랑', '와인',
       '해수욕장,해변', '민박', '치킨,닭강정', '베트남음식', '포장마차', '패션', '일본식주점', '오뎅,꼬치',
       '야식', '중식당', '회집', '닭발', '생선회', '요리주점', '전통,민속주점', '일식당', '횟집',
       '스포츠의류', '까페', '자연공원', '외국음식전문점(인도,태국등)', '종합분식', '치킨', '정육식당',
       '육류,고기', '북카페', '피자', '다방', '족발,보쌈', '기사식당', '곱창,막창', '해물,생선',
       '술집', '당구장,포켓볼', '갤러리카페', '곱창,막창,양', '미용', '퓨전음식', '해장국', '일본식라면',
       '국수', '찌개,전골', '음식점', '이탈리안', '김밥(도시락)', '디저트카페', '종합도소매',
       '통닭(치킨)', '탕류(보신용)', '뷔페식', '복어취급', '호텔', '슈퍼마켓', '주류', '한식뷔페',
       '한정식', '초밥,롤', '당구장', '장어', '향토음식', '프랑스음식', '퓨전요리', '일품순두부',
       '베이커리', '냉면', '닭요리', '바닷가재요리', '햄버거', '바(BAR)', '키즈카페,실내놀이터',
        , '다이어트,샐러드', '반찬가게', '전,빈대떡', '오리요리', '도시락,컵밥',
       '샤브샤브', '소고기구이', '회', '칼국수,만두', '스크린골프장', '장어,먹장어요리', '이자카야', '차',
       '미용실', '클럽하우스', '장례식장', '공영주차장', '아웃도어용품', '전기자동차 충전소', '매운탕,해물탕',
       '태국음식', '김밥', '유아동복', '감성주점', '퓨전일식', ', '패스트푸드', '과일,주스전문점',
       '판촉,기념품', , '뷔페', '인도음식', '곰탕', '숙박', '제과,베이커리', , '와인바',
       '스파게티,파스타전문', '막국수', '테이크아웃커피', '동남아음식', '주말농장', '음료,주류제조',
       , '출장조리',, '돈까스,우동', '', '전통찻집',
       '시도립병원', '라이브카페', '아이스크림', '골프용품', '백숙,삼계탕', '기업', '네일샵', '생활협동조합',
       '퓨전한식', '대게요리', '우동,소바', '편의점', '예식장', '종합병원', '지명', ,
       '사주카페', '비빔밥', '오리', '카페거리', '쌈밥', '도시락', '라면', '서핑,윈드서핑', '삼겹살',
       '갈비탕', '낙지요리', '', '생과일전문점', '중식', '닭갈비',  '고양이카페',
       '양갈비', '키즈카페', '', '칵테일바', '죽', '룸카페', '중고차', '순대,순댓국', '애견카페',
       '곰탕,설렁탕', '순대', '국밥', '두부요리', '구내식당',,
       '굴,전복', '백반,가정식', '추어탕', '감자탕', '덮밥', '만두', , 
       '체험마을', '멕시코,남미음식', '패밀리레스토랑', '샌드위치',, '푸드코트',
       , '아귀찜,해물찜', '일식집', ' '떡카페', '보드카페', ',
       '정육점', '여행사', '핫도그', ' '아시아음식', '일식튀김,꼬치', , 
       , '영화관',  '멕시칸,브라질', '식료품', '나이트,클럽', ,
   , '양꼬치', '스테이크,립', '설렁탕', '찜닭',
       , '스마일찹쌀꽈배기
       ,, '스페인음식', '커피숍', '기타 휴게음식점', '푸드트럭',
       '일반조리판매'],
       ],'''
jeju_Final_df[jeju_Final_df['업종구분소분류']=='키즈카페']

jeju_Final_df.drop(305,inplace=True)
jeju_Final_df.loc[2262]['업종구분소분류'] = '카페'
for i in a:
    jeju_Final_df.drop(i,inplace=True)

jeju_Final_df.loc[2262]['사업장명'] = 'BOHO'

jeju_Final_df.to_csv('C:/SEONWOO/jeju/jeju_Final_df2.csv',encoding='cp949',index =False)
jeju_Final_df

import pandas as pd
df_jeju = pd.read_csv('G:/내 드라이브/jeju/df_jeju.csv')

driver = webdriver.Chrome('C:/SEONWOO/chromedriver.exe') # 크롬드라이버로 열기 
time.sleep(2)
url = 'https://map.kakao.com/'                          # 네이버 맵 메인화면
driver.get(url)                                            # 크롬드라이버에 올리기
jeju_Gita
jeju_Gita.iloc[0:5,0:2]
time.sleep(2.7)
# 다음 카카오맵으로 재검색
import time
for i in range(0,2):
    road = ''.join(df_jeju.iloc[i]['도로명전체주소'].split(' ')[1:3])
    name = df_jeju.iloc[i]['사업장명']
    driver.find_element_by_class_name("input_search").clear() # 검색창 초기화 
    driver.find_element_by_class_name("input_search").send_keys(f'{name} {road}') # 상호명 검색 이 부분이 계속 바뀜.
    driver.find_element_by_class_name("input_search").send_keys(Keys.ENTER) # 엔터누르기 
    html = driver.current_url # 검색한 상호명 주소 따오기 
    res_code = re.findall(r"place/(\d+)", html)
    time.sleep(2.7)
    if res_code ==[]:
        pass
    else:
        final_url = 'https://pcmap.place.naver.com/restaurant/'+res_code[0]
        res =requests.get(final_url)
        res.encoding='utf-8'
        html_str = res.text
        soup = BeautifulSoup(html_str,'html.parser')
        stars = soup.select_one('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz > span._1Y6hi._1A8_M > em').text
        reviews = soup.select_one('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz > span:nth-child(2) > a > em').text
    if driver.find_element_by_class_name('noResultDesc').text == '검색어의 철자가 정확한지 다시 한번 확인해 주세요.\n장소를 찾을 때 전화번호, 주소도 활용해 보세요.':
        pass
    elif driver.find_element_by_class_name('addrtitle').text == '주소':
        pass
    else:
        driver.find_element(by=By.CLASS_NAME,value='score').text.split('\n')[1][:-1]
        driver.find_element(by=By.CLASS_NAME,value='review').text.split(' ')[1]
        driver.find_element(by=By.CLASS_NAME,value='txt_blind').text
pd.isnan(df_jeju['소재지전체주소'])
df_jeju[pd.isna(df_jeju['소재지전체주소'])]
pd.isna(df_jeju.iloc[4407]['소재지전체주소'])

from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re
import requests
options = wb.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정 # 코랩은 크롬창을 새로 안띄워준다.
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
url = 'https://map.naver.com/'
driver = wb.Chrome('C:/SEONWOO/chromedriver.exe', options=options)
driver.get(url)
df_jeju['n_reviews']=''
df_jeju['n_stars']=''
df_jeju['n_stars_vote']=''
1+1
for i in range(len(df_jeju)):
  name = df_jeju.iloc[i]['사업장명']
  addr = ''.join(df_jeju.iloc[i]['도로명전체주소'].split(' ')[1:3])
  driver.find_element(by=By.ID,value='search.keyword.query').clear() # 검색창 초기화 
  driver.find_element(by=By.ID,value="search.keyword.query").send_keys(f'{addr} {name} ') # 상호명 검색 이 부분이 계속 바뀜.
  driver.find_element(by=By.ID,value="search.keyword.query").send_keys(Keys.ENTER) # 엔터누르기 
  
  time.sleep(2.7)
  if driver.find_element(by=By.CLASS_NAME,value='noResultDesc').text == '검색어의 철자가 정확한지 다시 한번 확인해 주세요.\n장소를 찾을 때 전화번호, 주소도 활용해 보세요.':
    pass
  elif driver.find_element(by=By.CLASS_NAME,value='addrtitle').text == '주소':
    pass
  else:
    try:
      if driver.find_element(by=By.CLASS_NAME,value='txt_blind').text == '후기 미제공':
        pass
      else:
        stars = driver.find_element(by=By.CLASS_NAME,value='score').text.split('\n')[0]
        df_jeju['n_stars'][i] = stars
        stars_vote = driver.find_element(by=By.CLASS_NAME,value='score').text.split('\n')[1][:-1]
        df_jeju['n_stars_vote'][i] = stars_vote
        reviews = driver.find_element(by=By.CLASS_NAME,value='review').text.split(' ')[1]
        df_jeju['n_reviews'][i]=reviews
    except:
      pass
    print(i,df_jeju.iloc[i][['n_stars','n_stars_vote','n_reviews']])
for i in range(len(df_jeju)):
  if pd.isna(df_jeju.iloc[i]['소재지전체주소']):
    df_jeju['소재지전체주소'][i] = df_jeju.iloc[i]['도로명전체주소']  
for i in range(len(df_jeju)):
  if pd.isna(df_jeju.iloc[i]['도로명전체주소']):
    df_jeju['도로명전체주소'][i] = df_jeju.iloc[i]['소재지전체주소']
a=1
53*300
options = wb.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정 # 코랩은 크롬창을 새로 안띄워준다.
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
url = 'https://map.naver.com/' 
a=1155
df_jeju['사업장명'][1] ='그림책방&카페노란우산'
while(a<15901):
       
    x`x``
    a+=300
    
    
df_jeju.reset_index(level=None,drop=True)
df_jeju
df_jeju.to_csv('G:/내 드라이브/jeju/df_jeju_naver.csv',index=False)
