import streamlit as st 
import requests
import pandas as pd 
import arrow
import plotly.express as px 


response_assets = requests.get(f"https://api.coincap.io/v2/assets").json()["data"]
df_assets = pd.DataFrame.from_records(response_assets)
st.title('Тестовое Python: Saber Interactive')
st.write('Привет, это тестовое')
assets = df_assets.symbol
asset = st.sidebar.selectbox("Выбери коин", assets)
d1 = date_start = st.sidebar.date_input('Начало периода',key='d1',value=pd.to_datetime('2022-11-01'))
d2 = date_end = st.sidebar.date_input("Конец периода",key='d2',value=pd.to_datetime('2023-02-15'))
date_start_ts = int(arrow.get(date_start).timestamp()*1000)
date_end_ts = int(arrow.get(date_end).timestamp()*1000)
if st.sidebar.checkbox('Хочу сравнить с другой монетой'):
    asset_alt = st.sidebar.selectbox("Выбери альтернативный коин", assets)
    asset_real_alt = df_assets[df_assets.symbol==asset_alt].id.values[0]
    asset_real = df_assets[df_assets.symbol==asset].id.values[0]
    response_alt = requests.get(f"https://api.coincap.io/v2/assets/{asset_real_alt}/history?interval=d1&start={date_start_ts}&end={date_end_ts}").json()["data"]
    response = requests.get(f"https://api.coincap.io/v2/assets/{asset_real}/history?interval=d1&start={date_start_ts}&end={date_end_ts}").json()["data"]
    df = pd.DataFrame.from_records(response)
    df['coin'] = asset
    df_alt = pd.DataFrame.from_records(response_alt)
    df_alt['coin'] = asset_alt
    df_mrg = pd.concat([df,df_alt],axis=0)
    st.plotly_chart(px.line(df_mrg,x='date',y='priceUsd',color = 'coin',title=f"<br>История стоимости монеты {asset} против {asset_alt} </br>" ))
else: 
    asset_real = df_assets[df_assets.symbol==asset].id.values[0]
    response = requests.get(f"https://api.coincap.io/v2/assets/{asset_real}/history?interval=d1&start={date_start_ts}&end={date_end_ts}").json()["data"]
    df = pd.DataFrame.from_records(response)
    st.plotly_chart(px.line(df,x='date',y='priceUsd',title=f"<br>История стоимости монеты {asset} </br>" ))