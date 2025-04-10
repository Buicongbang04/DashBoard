import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
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
    filter_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filter_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filter_df = df3[df3["City"].isin(city)]
else:
    filter_df = df3[df3['Region'].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

category_df = filter_df.groupby(['Category'], as_index=False)["Sales"].sum()
category_df['Formatted_Sales'] = category_df['Sales'].apply(lambda x: f"${x:,.2f}")


with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(
        category_df,
        x='Category',
        y='Sales',
        text='Formatted_Sales',
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Region wise Sales")
    fig = px.pie(filter_df, values='Sales', names='Region', hole=0.5)
    fig.update_traces(text=filter_df['Region'], textposition='outside')
    st.plotly_chart(fig, use_container_width=True, height=200)


cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category View Data"):
        st.write(category_df.style.background_gradient(cmap='Blues'))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download CSV", data=csv, file_name='category.csv', mime='text/csv',
                           help='Click here to download the data in CSV format')
with cl2:
    with st.expander("Region View Data"):
        region_df = filter_df.groupby(['Region'], as_index=False)["Sales"].sum()
        region_df['Formatted_Sales'] = region_df['Sales'].apply(lambda x: f"${x:,.2f}")
        st.write(region_df.style.background_gradient(cmap='Oranges'))
        csv = region_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download CSV", data=csv, file_name='region.csv', mime='text/csv',
                           help='Click here to download the data in CSV format')
        

# Time Series Analysis
filter_df['month_year'] = filter_df['Order Date'].dt.to_period('M').astype(str)
st.subheader("Time Series Analysis")
lineChart = pd.DataFrame(filter_df.groupby(['month_year'], as_index=False)["Sales"].sum()).reset_index(drop=True)
fig2 = px.line(lineChart, x='month_year', y='Sales', labels={'Sales':'Amount'},
               height=500, width=1000,template='gridon')
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Time Series Data"):
    st.write(lineChart.T.style.background_gradient(cmap='Greens'))
    csv = lineChart.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download CSV", data=csv, file_name='time_series.csv', mime='text/csv',
                       help='Click here to download the data in CSV format')

# Create a tree map base on Region, Category and Sub-Category
st.subheader("Hierarchical view of Sales using Tree Map")
fig3 = px.treemap(filter_df, path=['Region', 'Category', 'Sub-Category'], values='Sales', hover_data=['Sales'],
                  color='Sub-Category', template='plotly_dark')
fig3.update_layout(width=800, height=650)
st.plotly_chart(fig3, use_container_width=True)

chart1, chart2 = st.columns(2)
with chart1:
    st.subheader("Segment wise Sales")
    fig = px.pie(filter_df, values='Sales', names='Segment', template='plotly_dark')
    fig.update_traces(text=filter_df['Segment'], textposition='inside')
    st.plotly_chart(fig, use_container_width=True, height=200)

with chart2:
    st.subheader("Category wise Sales")
    fig = px.pie(filter_df, values='Sales', names='Category', template='plotly_dark')
    fig.update_traces(text=filter_df['Category'], textposition='inside')
    st.plotly_chart(fig, use_container_width=True, height=200)

st.subheader(":point_right: Month wise Sub-category Sales summary")
with st.expander("Summary Table"):
    df_sample = df[0:5][['Region', 'State', 'City', 'Category', 'Sales', 'Profit', 'Quantity']]
    fig = ff.create_table(df_sample, colorscale='cividis')
    st.plotly_chart(fig, use_container_width=True, height=200)

    st.markdown("Month wise Sub-category Table")
    filter_df['month'] = filter_df['Order Date'].dt.month_name()
    sub_category_year = pd.pivot_table(filter_df, values='Sales', index=['Sub-Category'], columns='month').reset_index()
    st.write(sub_category_year.style.background_gradient(cmap='Reds'))

# Create a scatter plot
data1 = px.scatter(filter_df, x='Sales', y='Profit', size='Quantity', template='plotly_dark')
data1.update_layout(
    title=dict(
        text='Sales vs Profit',
        font=dict(size=25)
    ),
    xaxis=dict(
        title=dict(
            text='Sales',
            font=dict(size=19)
        )
    ),
    yaxis=dict(
        title=dict(
            text='Profit',
            font=dict(size=19)
        )
    )
)
st.plotly_chart(data1, use_container_width=True)

with st.expander("View Data"):
    st.write(filter_df.iloc[:500, 1:20:2].style.background_gradient(cmap='Accent'))

# Download original data
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Original Data", data=csv, file_name='original_data.csv', mime='text/csv',
                   help='Click here to download the data in CSV format')