# a = 12
# b='1234'
# print('%06d,%s' %(a ,b))
# if a > 18:
#     print('18');
# if a < 18:
#     print('%d' %a);
# i = 1;
# while i < 10:
#     j = 1;
#     while j <= i:
#         print('%d * %d = %d' %(i,j,i*j),end='\t');
#         j = j + 1;
#     print('');
#     i = i + 1;
# name_list = [];
# name = input("请输入您的昵称:");
# if name in name_list:
#     print("您输入的昵称{name}已存在".format(name));
# else:
#     print("成功")
#     name_list.append(name);

# import requests
# from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
#
# url = 'https://music.163.com/#/discover/toplist'
# headers = {
#     'user-agent:':UserAgent().random
# }
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())
#
# from selenium import webdriver
# import time
# driver = webdriver.Edge();
# driver.get("http://www.baidu.com");
# time.sleep(1);
# driver.maximize_window()
#
# time.sleep(3);
# driver.quit();

 # import pandas as pd
# data = pd.read_table('E:\python项目\ext.txt',header=1, delimiter=',', encoding='utf-8')
# print(data.head(2))
# print(type(data))


import pandas as pd
import numpy as np

cust_number = {'年份':['2022','2021','2020','2019'],'月份':['1月','2月','3月','4月'],'ad':[10,11,12,13],'tel':[49,50,51,52],'srch':[38,45,50,43],'intr':[25,19,25,22]}

print(type(cust_number))
cust_number = pd.DataFrame(cust_number)

cust = cust_number.iloc[1:3]
print(cust)
print(cust_number.index)
print(cust_number.columns)
cust1 = cust_number.set_index(['月份'])
print(cust1)



df3 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'], 'B': ['B4', 'B5', 'B6', 'B7'],
                    'C': ['C4', 'C5', 'C6', 'C7'], 'D': ['D4', 'D5', 'D6', 'D7']})

df4 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'], 'B': ['B8', 'B9', 'B10', 'B11'],
                    'C': ['C8', 'C9', 'C10', 'C11'], 'D': ['D8', 'D9', 'D10', 'D11']})

# 使用 concat 函数垂直拼接 df3 和 df4
result = pd.concat([df3, df4], ignore_index=True)
print(result)

# 水平拼接
result_horizontal = pd.concat([df3, df4], axis=1)
print(result_horizontal)










