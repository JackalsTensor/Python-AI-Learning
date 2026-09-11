import numpy as np
import pandas as pd
df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle泰坦尼克号传送维度赛事数据集\train.csv")
print(df.columns)
print(df.info())
"""
Index([PassengerId（乘客 ID）HomePlanet（出发星球）CryoSleep（低温休眠状态）
Cabin（船舱号）Destination（目的地星球）Age（年龄）VIP（VIP 会员）RoomService（客房服务消费）
FoodCourt（美食广场消费）ShoppingMall（购物中心消费）Spa（水疗消费）VRDeck（VR 平台消费）
Name（姓名）Transported（是否成功传送],
      dtype='object')           
      
#   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   PassengerId   8693 non-null   object 
 1   HomePlanet    8492 non-null   object 
 2   CryoSleep     8476 non-null   object 
 3   Cabin         8494 non-null   object 
 4   Destination   8511 non-null   object 
 5   Age           8514 non-null   float64
 6   VIP           8490 non-null   object 
 7   RoomService   8512 non-null   float64
 8   FoodCourt     8510 non-null   float64
 9   ShoppingMall  8485 non-null   float64
 10  Spa           8510 non-null   float64
 11  VRDeck        8505 non-null   float64
 12  Name          8493 non-null   object 
 13  Transported   8693 non-null   bool   
dtypes: bool(1), float64(6), object(7)
memory usage: 891.5+ KB
None
"""

#分别查看缺失率
age_total = len(df['Age'])
age_missing = df['Age'].isnull().sum()
age_missing_rate = age_missing / age_total * 100
print(f'age缺失率：{age_missing_rate:.2f}%')

room_service_total = len(df['RoomService'])
room_service_missing = df['RoomService'].isnull().sum()
room_service_missing_rate = room_service_missing / room_service_total * 100
print(f'RoomService缺失率：{room_service_missing_rate:.2f}%')