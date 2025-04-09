import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")



st.set_page_config(
    page_title="Super Store Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title(":bar_chart: Super Store Dashboard EDA")
st.markdown('<style>div.block-container{padding-top:35px;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload file", type=["csv", "txt", "xlsx", "xls"])
if fl is not None:
    filename = fl.name
    st.write(f"File name: {filename}")
    df = pd.read_excel(filename)
else:
    os.chdir(r'D:\Study\Python\Interactive_Dashboard\data')
    df = pd.read_excel('Sample - Superstore.xls')

col1, col2 = st.columns(2)
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Getting the min and max date
startDate = pd.to_datetime(df['Order Date']).min()
endDate = pd.to_datetime(df['Order Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)].copy()

st.sidebar.header("Filter: ")

# Create for region
region = st.sidebar.multiselect("Pick your region: ", 
                                df['Region'].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]

# Create for State
state = st.sidebar.multiselect("Pick your state: ", 
                                df2['State'].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]

# Create for City
city = st.sidebar.multiselect("Pick your city: ", 
                                df3['City'].unique())

# Filter the data based on Region, State and City
if not region and not state and not city:
    filter_df = df
elif not state and not city:
    filter_df = df[df['Region'].isin(region)]
elif not region and not city:
    filter_df = df[df['State'].isin(state)]
elif not region and not state:
    filter_df = df[df['City'].isin(city)]
elif state and city:
    filter_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filter_df = df3[df["State"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filter_df = df3[df["State"].isin(region) & df3["City"].isin(state)]
elif city:
    filter_df = df3[df3["City"].isin(city)]
else:
    filter_df = df3[df3['Region'].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]