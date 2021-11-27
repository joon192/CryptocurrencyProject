# -*- coding: utf-8 -*-


import warnings
warnings.filterwarnings('ignore')
import time
import datetime
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns

import itertools
import operator

import base64
from io import BytesIO

from datetime import datetime, timedelta

def Recommendation_DB():
 
  n = [7,30,90,180]
  crypto_name = ['ADA','BTC','BCH','DOGE','EOS','ETH','OMG','SNT','XRP']
  bounds = [7,30,180,360,720]

  for i in crypto_name:
    db = pymysql.connect(host='35.76.154.105', port=3306, user='root', passwd='1234',db='upbit', charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM {0}'.format(i)
    cursor.execute(sql)
    result = cursor.fetchall()
    globals()[f'{i}'] = pd.DataFrame(result)

  crypto = [ADA,BTC,BCH,DOGE,EOS,ETH,OMG,SNT,XRP]

  for i,j in zip(crypto_name, crypto):
    globals()[i] = j.loc[::-1].reset_index()
    print('완료:', i)

    
  daily_engine = create_engine("mysql+mysqldb://root:1234@35.76.154.105:3306/Recommendation", encoding='utf-8',pool_size = 100000,max_overflow = 0)

  for j in crypto :
    for i in n:
      j['이동평균{0}일'.format(i)]= j['close'].rolling(window=i).mean().shift(-(i-1))

  for j in crypto:
    for i in n :
      j['이동평균{0}일표준편차'.format(i)]= j['close'].rolling(window=i).std().shift(-(i-1))
    for i in n :
      j['이동평균{0}일z밸류'.format(i)] = (j['close']-j['이동평균{0}일'.format(i)])/(j['이동평균{0}일표준편차'.format(i)])

  for j in crypto:
    for i in n :
      j['이동평균{0}일z밸류제곱'.format(i)] = j['이동평균{0}일z밸류'.format(i)]**2

  DF = dict()
  for l,k in zip(crypto_name,crypto):
    for j in n:
      for i in bounds:
       DF['{2};MA{1};bounds{0};'.format(i,j,l)] = np.sqrt(k['이동평균{0}일z밸류제곱'.format(j)][0:i].mean())

  for k in n:
    for j in bounds :

      DFX = []

      for i in DF.keys():
        if i.find('bounds{0};'.format(j)) >= 0:
          if i.find('MA{0};'.format(k)) >= 0 :

           a = i.split(';')[0]
           b = i.split(';')[1]
           c = i.split(';')[2]
           d = DF.get(i)
           data = [a,b,c,d]
           DFX.append(data)
      dfx = pd.DataFrame(DFX)
      dfx.columns = ['crypto','MA','bounds','z_value']
      dfx['z_value_rank']=dfx['z_value'].rank(method='max')
      # dfx.to_csv('/content/drive/MyDrive/Colab Notebooks/datasets/test/MA{0}_bounds{1}_.csv'.format(k,j), index =False)
      daily_conn = daily_engine.connect()
      dfx.to_sql(name='MA{0}_bounds{1}_'.format(k,j),con=daily_conn,if_exists='replace')
      print(' 업데이트 완료:', 'MA{0}_bounds{1}_'.format(k,j), '\n' )

Recommendation_DB()

"""## II.Output 함수"""

#함수 정의
def amplitude_level_output_ranking(zvalue,alevel):
  crypto = [ADA,BTC,BCH,DOGE,EOS,ETH,OMG,SNT,XRP]
  Ranking = -abs(zvalue-alevel) + len(crypto)
  return Ranking

def input_n_bounds_alevel_output_crypto(n,bounds,input_amplitude_level_p,input_amplitude_level_s):
  
  crypto = [ADA,BTC,BCH,DOGE,EOS,ETH,OMG,SNT,XRP]
  crypto_name = ['ADA','BTC','BCH','DOGE','EOS','ETH','OMG','SNT','XRP']
  
  input_amplitude_level_p = input_amplitude_level_p*9/5
  input_amplitude_level_s = input_amplitude_level_s*9/5

  db_p = pymysql.connect(host='35.76.154.105', port=3306, user='root', passwd='1234',db='Recommendation', charset='utf8')
  cursor = db_p.cursor(pymysql.cursors.DictCursor)
  sql_p = 'SELECT * FROM MA{0}_bounds{1}_'.format(n,bounds)
  cursor.execute(sql_p)
  result_p = cursor.fetchall()
  out_DF_p = pd.DataFrame(result_p)
  # out_DF_p = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/datasets/test/MA{0}_bounds{1}_.csv'.format(n,bounds))
  db_s = pymysql.connect(host='35.76.154.105', port=3306, user='root', passwd='1234',db='Recommendation2', charset='utf8')
  cursor = db_s.cursor(pymysql.cursors.DictCursor)
  sql_s = 'SELECT * FROM sentimental'
  cursor.execute(sql_s)
  result_s = cursor.fetchall()
  out_DF_s = pd.DataFrame(result_s)
  # out_DF_s = pd.read_csv(''/content/drive/MyDrive/Colab Notebooks/datasets/cryptocurrency_sentiment/sentimental.csv')



  coustomer_finalscore_p = {}

  for j,i in zip(out_DF_p['crypto'],out_DF_p['z_value_rank']):
    # print(j,i)
    coustomer_finalscore_p[j] = amplitude_level_output_ranking(i,input_amplitude_level_p)


  coustomer_finalscore_s = {}

  for j,i in zip(out_DF_s['crypto'],out_DF_s['z_value_rank']):
    coustomer_finalscore_s[j] = amplitude_level_output_ranking(i,input_amplitude_level_s)
    # print(coustomer_finalscore[j])

  coustomer_finalscore = {}

  for i in crypto_name :
    p = coustomer_finalscore_p['{0}'.format(i)]
    a = coustomer_finalscore_s['{0}'.format(i)]
    F = p+a
    coustomer_finalscore[i] = F
    print('완료',i,F)

    out_put = max(coustomer_finalscore,key=coustomer_finalscore.get)
    # print(out_put)

  for i in range(len(out_DF_p)):
    if out_DF_p['crypto'][i] == out_put:
      z_value_rank_p = out_DF_p['z_value_rank'][i]

  for i in range(len(out_DF_s)):
    if out_DF_s['crypto'][i] == out_put:
      z_value_rank_s = out_DF_s['z_value_rank'][i]  

  cryptoN = len(crypto_name)

  return out_put, n, bounds, int(z_value_rank_p), int(z_value_rank_s), cryptoN

#out : {1}, n : {2}, bounds: {3}, p-value:{4}, s-value:{5}, cry:{6}