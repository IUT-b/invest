import os
import streamlit as st
from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime

# st.title('積立投資シミュレーション')
# st.header('積立投資・ドルコスト平均法シミュレーション')
st.write('積立投資・ドルコスト平均法のシミュレーション')

# 投資先選択
invest = st.sidebar.radio('投資先',['ダウ平均株価', 'QQQ'])
if invest=='ダウ平均株価':
    invest='NY Dow'
    invest2='^DJI'
elif invest=='QQQ':
    invest='QQQ'
    invest2='QQQ'
# elif invest=='ナスダック総合指数':
#     invest='NASDAQ'
#     invest2='^NDQ'

# 条件入力
savings = st.sidebar.number_input(label='最初の貯金額（ドル）',value=10000,step=1000)
purchase = st.sidebar.number_input(label='最初の投資額（ドル）',value=1000,step=1000)
purchases = st.sidebar.number_input(label='積立金額（ドル／月）',value=100,step=100)

# 株価取得期間
start_original = dt.date(year=1975,month=1,day=1)
end_original = dt.datetime.now().date()

# シミュレーション期間入力
start, end  = st.slider('シミュレーション期間', 
                   format='YYYY/MM',
                   min_value=start_original, 
                   value=(end_original-relativedelta(years=10),
                   end_original),
                   max_value=end_original
                   # step=relativedelta(months=1)
                  )

# 全期間データ
df_original=data.DataReader(invest2,'stooq',start_original,end_original)
df_original=df_original.iloc[::-1]
date_original=df_original.index

# 選択期間データ
df=df_original[start:end]
date=df.index

# 積立日データ
df2=df.reset_index()
df2 = df2.groupby([df2['Date'].dt.year, df2['Date'].dt.month]).head(1)
df2.set_index('Date',inplace = True)

# 積立計算
df['purchases']=0
df.loc[df2.index,'purchases']=purchases
df.iloc[0,df.columns.get_loc('purchases')]=df.iloc[0,df.columns.get_loc('purchases')]+purchase
df['total_purchases']=df['purchases'].cumsum()
df['shares']=df['purchases']/df['Close']
df['total_shares']=df['shares'].cumsum()
df['value']=df['Close']*df['total_shares']+savings

# グラフ
fig = plt.figure()
plt.subplots_adjust(hspace=0.6)
ax1 = fig.add_subplot(2,1,1)
ax1.plot(date_original, df_original['Close'],label=invest,color='black')
ax1.set_title(invest)
ax1.set_ylabel(invest+'(USD)')
ax1.legend()
# ax1.legend(prop = {"family" : "MS Gothic"})
ax1.grid()
ax1.tick_params(labelsize=7)
ax2 = fig.add_subplot(2,1,2)
ax2.set_title('simulation')
ax2.set_xlabel('date')
ax2.set_ylabel(invest+'(USD)')
ax3 = ax2.twinx()
ax3.set_ylabel('investment,appraised amount(USD)')
ax2.plot(date, df['Close'],label=invest,color='black')
ax2.grid()
ax2.tick_params(labelsize=7)
ax3.plot(date, df['total_purchases']+savings,label='investment amount',color='blue')
ax3.plot(date, df['value'],label='appraised amount',color='red')
ax3.legend()
ax3.tick_params(labelsize=7)
st.pyplot(fig)







# def sim(start,end,purchases):
#     df=data.DataReader('^DJI','stooq',start,end)
#     df=df.iloc[::-1]
#     date=df.index
#     df['purchases']=purchases
#     df['total_purchases']=df['purchases'].cumsum()
#     df['shares']=df['purchases']/df['Close']
#     df['total_shares']=df['shares'].cumsum()
#     df['value']=df['Close']*df['total_shares']
#     fig = plt.figure()
#     ax1 = fig.subplots()
#     ax2 = ax1.twinx()
#     ax1.plot(date, df['Close'])
#     ax2.plot(date, df['total_purchases'])
#     ax2.plot(date, df['value'])
#     st.pyplot(fig)

# # sim(start,end,purchases)

# if st.button('開始'):
#     sim(start,end,purchases)





    