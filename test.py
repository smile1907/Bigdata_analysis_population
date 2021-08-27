#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from pandas.core.frame import DataFrame


# In[2]:


# 데이터 입력및 기본처리 (함수화 예정)
data1 = pd.read_excel("c://python//아파트_실거래가_test.xlsx")
print(data1.head())


# In[3]:


data2 = data1.drop(columns=["번지","본번","부번","단지명","층","도로명","건축년도","해제사유발생일"])
print(data2.head())


# In[4]:


# 사용할 정보 가공 (함수와 예정)
dali = [] #시군구에서 시에 대한 정보만 추출
for da in data2["시군구"]:
    dali.append(da.split(" ")[1]) #0 : 도 , 1 : 시
data2["시"] = dali #시군구는 놔두고 시를 새로 생성
print(data2.head())


# In[5]:


cha = [] # 창원시는 여러개의 구로 나누어진 형태로 이를 창원시로 병합
for i in data2["시"]:
    if i[0:2] == "창원":
        cha.append("창원시")
    else:
        cha.append(i)
data2["시"] = cha


# In[6]:


# 가공된 데이터에서 필요한 지역만을 가져옴 (완성본에서는 불필요)
data3 = data2[data2["시"] == "김해시"]
print(data3.head())


# In[8]:


dali2 = [] # 거래금액은 띄어쓰기와 ,로 인해서 문자열로 지정된 상태
k = "" # 여기서 띄어쓰기와 ,를 지우고 정수형으로 변환해 저장
for i in data3["거래금액(만원)"]:
    for j in i:
        if j != " " and j != ",":
            k = k + j
    dali2.append(int(k))
    k = ""

data3["돈"] = dali2 # 돈이라는 새로운 배열을 만듦
print(data3.info(),data3["돈"].mean(),data3["돈"].min(),data3["돈"].max()) # 정보, 평균, 최소, 최대값 표시


# In[9]:


# 지역별 아파트 가격차이를 시각화 하기 위한 데이터 선별 (함수화 예정)
data5 = pd.DataFrame() # 빈 데이터 프레임
data5["시"] = data2["시"]

dali3 = [] # 문자열인 금액의 데이터를 정수형으로 변환
k = ""
for i in data2["거래금액(만원)"]:
    for j in i:
        if j != " " and j != ",":
            k = k + j
    dali3.append(int(k))
    k = ""
data5["돈"] = dali3
print(data5)


# In[10]:


# 데이터를 시각화하기 위해서 각 시별로 그룹핑한 다음 평균을 적용
data4 = data5.groupby("시",as_index=False).apply(lambda x: x.mean())
print(data4)


# In[11]:


# 그래프 출력 (함수화 필요할 가능성 있음)
font_dirs = [r'C:\Users\Administrator\AppData\Local\Microsoft\Windows\Fonts', ] # 폰트 경로
font_files = fm.findSystemFonts(fontpaths=font_dirs) # 경로 추적
for font_file in font_files:# 경로 내의 폰트 저장
    fm.fontManager.addfont(font_file)


# In[12]:


plt.figure(figsize=(10,5))
sns.set(font="NanumGothic", # 폰트 나눔고딕
        rc={"axes.unicode_minus":False}, # 마이너스 부호 깨짐 방지
        style='darkgrid') # 검은 그리드
#plt.bar(data4["시"],data4["돈"])
order_1 = data5.groupby('시')['돈'].median().sort_values(ascending = False).index
sns.boxplot(x='시',y='돈',data=data5,orient='v',order= order_1)
plt.show()


# In[ ]:




