import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import requests
import psycopg2
from PIL import Image


### SQL Connection ###

mydb = psycopg2.connect(host="localhost", user="postgres", password="ananya14", port="5432", database="phonepe_data")
cursor = mydb.cursor()

### Data Frame creation from SQL ###

# Aggregated Insurance DataFrame

cursor.execute("select * from aggregated_insurance;")
mydb.commit()
table1 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

# Aggregated Transaction DataFrame

cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table2 = cursor.fetchall()

Aggre_transaction = pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

# Aggregated User DataFrame

cursor.execute("select * from aggregated_user;")
mydb.commit()
table3 = cursor.fetchall()

Aggre_user = pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))

# Map Insurance DataFrame

cursor.execute("select * from map_insurance;")
mydb.commit()
table4 = cursor.fetchall()

map_insurance = pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

# Map Transaction DataFrame

cursor.execute("select * from map_transaction;")
mydb.commit()
table5 = cursor.fetchall()

map_transaction = pd.DataFrame(table5,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

# Map User DataFrame

cursor.execute("select * from map_user;")
mydb.commit()
table6 = cursor.fetchall()

map_user = pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","Registered_users","App_opens"))

# Top Insurance DataFrame

cursor.execute("select * from top_insurance;")
mydb.commit()
table7 = cursor.fetchall()

top_insurance = pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

# Top Transaction DataFrame

cursor.execute("select * from top_transaction;")
mydb.commit()
table8 = cursor.fetchall()

top_transaction = pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

# Top User DataFrame

cursor.execute("select * from top_user;")
mydb.commit()
table9 = cursor.fetchall()

# Functions for Analysis and visualization

top_user = pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))

def Transaction_amount_amount_Y(df,year):

    state_name_mapping = {
        "Andaman & Nicobar Islands": "Andaman & Nicobar",
        "Andaman & Nicobar Island": "Andaman & Nicobar",
        # Add any other necessary mappings here
    }

    # Apply the mapping to the 'States' column
    df["States"] = df["States"].replace(state_name_mapping)

    
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
         fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year} Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
         st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year} Transaction Count",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{year} Transaction Amount", fitbounds="locations",
                                height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{year} Transaction Count", fitbounds="locations",
                                height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

        return tacy


def Transaction_amount_amount_Y_Q(df, quater):
     # Map inconsistent state names in the DataFrame to match the GeoJSON names
    state_name_mapping = {
        "Andaman & Nicobar Islands": "Andaman & Nicobar",
        "Andaman & Nicobar Island": "Andaman & Nicobar",
        # Add any other necessary mappings here
    }

    # Apply the mapping to the 'States' column
    df["States"] = df["States"].replace(state_name_mapping)
    tacy = df[df["Quarter"] == quater]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} Year {quater} Quarter Transaction Amount",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} Year {quater} Quarter Transaction Count",
                           color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    # Fetching geojson data
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    states_name.sort()

    # Ensure locations matches the number of unique states in tacyg
    locations =tacyg["States"]

    # Plot choropleth maps
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].min()),
                                    hover_name="States",
                                    title=f"{tacy['Years'].min()} Year {quater} Quarter Transaction Amount",
                                    fitbounds="locations",
                                    height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].min()),
                                    hover_name="States",
                                    title=f"{tacy['Years'].min()} Year {quater} Quarter Transaction Count",
                                    fitbounds="locations",
                                    height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Aggre_Tran_Transaction_type(df,state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_pie1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",
                        width=600,height=600,title=f"{state.upper()} Transaction Amount",hole=0.5,color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_pie1)

    with col2:
        fig_pie2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",
                        width=600,height=600,title=f"{state.upper()} Transaction Count",hole=0.5,color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_pie2)
    
def Aggre_user_plot_1(df,year):
    aguy = df[df["Years"] == year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year} Brands and Transaction Count",
                     width=1000,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    return aguy

#Aggregated User Analysis
def Aggre_user_plot_2(df,quarter):

    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop=True, inplace=True)
    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quarter} Quarter Brands and Transaction Count",
                        width=1000,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

# Aggregated User Analysis 3
def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1=px.line(auyqs,x="Brands",y="Transaction_count",hover_data=["Percentage"],
                    title=f"{state} Brands, Transaction Count, Percentage",
                        width=1000,color_discrete_sequence=px.colors.sequential.Aggrnyl,markers=True)

    st.plotly_chart(fig_line_1)
# Map Insurance District
def Map_insur_District(df,state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_bar1=px.bar(data_frame=tacyg,x="Transaction_amount",y="Districts",orientation="h",
                        title=f"{state} District and Transaction Amount",color_discrete_sequence=px.colors.sequential.Aggrnyl)
                        
        st.plotly_chart(fig_bar1)
    with col2:
        fig_bar2=px.bar(data_frame=tacyg,x="Transaction_count",y="Districts",orientation="h",
                        title=f"{state} District and Transaction Count",color_discrete_sequence=px.colors.sequential.Aggrnyl)
                        
        st.plotly_chart(fig_bar2)

        return tacy
# Map user plot 1
def map_user_plot_1(df,year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop=True, inplace=True)

    muyg = muy.groupby("States")[["Registered_users","App_opens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg,x="States",y=["Registered_users","App_opens"],
                    title=f"{year} Year Registered User and App Opens",
                        width=1000,height= 800,markers=True)
    st.plotly_chart(fig_line_1)

    return muy
# Map user plot 2
def map_user_plot_2(df,quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg = muyq.groupby("States")[["Registered_users","App_opens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg,x="States",y=["Registered_users","App_opens"],
                    title=f"{df['Years'].min()} Year {quarter} Quarter Registered User and App Opens",
                        width=1000,height= 800,markers=True,color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq
# Map User Plot 3
def map_user_plot_3(df,states):
    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop=True, inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_map_user_bar_1=px.bar(data_frame=muyqs,x="Registered_users",y="Districts",orientation="h",
                                title=f"{states} Registered Users",height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2: 
        fig_map_user_bar_2=px.bar(data_frame=muyqs,x="App_opens",y="Districts",orientation="h",
                                title=f"{states} App Opens",height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_2)
# Top Insurance Plot 1
def Top_insur_plot_1(df,state):
    tiy = df[df["States"] == state]
    tiy.reset_index(drop=True, inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_top_insur_bar_1=px.bar(data_frame=tiy,x="Quarter",y="Transaction_amount",hover_data="Pincodes",
                                title="Transaction Amount",height=500,color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_top_insur_bar_1)
    with col2:
        fig_top_insur_bar_2=px.bar(data_frame=tiy,x="Quarter",y="Transaction_count",hover_data="Pincodes",
                                title="Transaction Count",height=500,color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)   
        return tiy
# Top User Plot 1
def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States" , "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)
    fig_top_plot_1=px.bar(data_frame=tuyg,x="States",y="RegisteredUsers",color="Quarter",width=1000,height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",
                        title=f"{year} Year Registered Users")
    st.plotly_chart(fig_top_plot_1)

    return tuy
# Top User Plot 2
def top_user_plot_2(df,state):
    tuys=df[df["States"] == state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2=px.bar(data_frame=tuys,x="Quarter",y="RegisteredUsers",title="Registered Users, Pincodes, Quarter",
                        width=1000,height=800,color="RegisteredUsers",hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Rainbow_r)                    
    st.plotly_chart(fig_top_plot_2)

# SQL Connection

def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="ananya14", port="5432", database="phonepe_data")
    cursor = mydb.cursor()

    # plot 1
    query1=f'''select states, sum(transaction_amount) as transaction_amount from {table_name} group by states order by transaction_amount desc limit 10; '''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=('states','transaction_amount'))
    col1, col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="states",y="transaction_amount",title="Top 10 states with highest transaction amount",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2=f'''select states, sum(transaction_amount) as transaction_amount from {table_name} group by states order by transaction_amount limit 10; '''

    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=('states','transaction_amount'))


    with col2:
        fig_amount2=px.bar(df_2,x="states",y="transaction_amount",title="Top 10 states with lowest transaction amount",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''SELECT states, AVG(transaction_amount) AS avg_transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY avg_transaction_amount;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('states','transaction_amount'))

    fig_amount3=px.bar(df_3,x="transaction_amount",y="states",title="Average Amount of transaction",hover_name="states",orientation="h",
                    height=500,width=1000)
    st.plotly_chart(fig_amount3)

def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="ananya14", port="5432", database="phonepe_data")
    cursor = mydb.cursor()

    # plot 1
    query1=f'''select states, sum(transaction_count) as transaction_count from {table_name} group by states order by transaction_count desc limit 10; '''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=('states','transaction_count'))

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(df_1,x="states",y="transaction_count",title="Top 10 states with highest transaction count",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2=f'''select states, sum(transaction_count) as transaction_count from {table_name} group by states order by transaction_count limit 10; '''

    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    with col2:
        df_2=pd.DataFrame(table2,columns=('states','transaction_count'))

        fig_amount2=px.bar(df_2,x="states",y="transaction_count",title="Top 10 states with lowest transaction count",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''SELECT states, AVG(transaction_count) AS avg_transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY avg_transaction_count;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('states','transaction_count'))

    fig_amount3=px.bar(df_3,x="transaction_count",y="states",title="Average Amount of transaction count",hover_name="states",orientation="h",
                    height=500,width=1000)
    st.plotly_chart(fig_amount3)

# from qn 7 to 10

def top_chart_registered_user(table_name,state):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="ananya14", port="5432", database="phonepe_data")
    cursor = mydb.cursor()

    # plot 1
    query1= f'''select districts, sum(registeredusers) as registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=('Districts','Registeredusers'))

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.bar(df_1,x="Districts",y="Registeredusers",title="Top 10 Districts with Registered users",hover_name="Districts",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2= f'''select districts, sum(registeredusers) as registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers
                limit 10;'''
    
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=('Districts','Registeredusers'))

    with col2:

        fig_amount2=px.bar(df_2,x="Districts",y="Registeredusers",title="Top 10 Districts with lowest Registered users",hover_name="Districts",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''select districts, avg(registeredusers) as registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('Districts','Registeredusers'))

    fig_amount3=px.bar(df_3,x="Registeredusers",y="Districts",title="Average of Registered Users",hover_name="Districts",orientation="h",
                    height=500,width=500)
    st.plotly_chart(fig_amount3)

#qn 9
# SQL Connection

def top_chart_appopens(table_name,state):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="ananya14", port="5432", database="phonepe_data")
    cursor = mydb.cursor()

    # plot 1
    query1= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens desc
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=('Districts','appopens'))

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.bar(df_1,x="Districts",y="appopens",title="Top 10 Districts with App Opens",hover_name="Districts",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens
                limit 10;'''
    
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=('Districts','appopens'))

    with col2:
        fig_amount2=px.bar(df_2,x="Districts",y="appopens",title="Top 10 Districts with lowest App Opens",hover_name="Districts",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''select districts, avg(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('Districts','appopens'))

    fig_amount3=px.bar(df_3,x="appopens",y="Districts",title="Average of App Opens",hover_name="Districts",orientation="h",
                    height=500,width=500)
    st.plotly_chart(fig_amount3)
# qn 10
# SQL Connection

def registered_user_top_chart(table_name):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="ananya14", port="5432", database="phonepe_data")
    cursor = mydb.cursor()

    # plot 1
    query1= f'''select states,sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    col1,col2=st.columns(2)

    with col1:
        df_1=pd.DataFrame(table,columns=('states','registeredusers'))

        fig_amount=px.bar(df_1,x="states",y="registeredusers",title="Top 10 Registered Users",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2= f'''select states,sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers
                limit 10;'''
    
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=('states','registeredusers'))

    with col2:

        fig_amount2=px.bar(df_2,x="states",y="registeredusers",title="Last 10 Registered Users",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''select states,avg(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('states','registeredusers'))

    fig_amount3=px.bar(df_3,x="registeredusers",y="states",title="Average of App Opens",hover_name="states",orientation="h",
                    height=500,width=500)
    st.plotly_chart(fig_amount3)

### Streamlit Application Code ###

st.set_page_config(layout="wide")
st.title(":violet[Phonepe Pulse Data Analysis]")

with st.sidebar:

    selected = option_menu(
        menu_title=None,
        options=["Home", "Data Exploration", "Top Charts"],
        icons=["house", "bar-chart", "geo"],
        menu_icon="cast",
        default_index=0,
    )

def setting_bg():
   
   st.markdown(f""" <style>.stApp {{
                        background:url("https://static.vecteezy.com/system/resources/previews/004/838/359/large_2x/dark-purple-grunge-abstract-concrete-wall-texture-background-free-photo.jpg");
                        background-size:cover}}
                     </style>""", unsafe_allow_html=True)
                    # https://wallpapers.com/images/high/purple-and-black-background-9a0om5bk62fizm2m.webp
   
setting_bg()

if selected == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.video("https://www.phonepe.com/webstatic/6508/videos/page/home-fast-secure-v3.mp4")

    with col2:
        st.header(":red[PHONEPE]")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown(":blue[To offer every Indian equal opportunity to accelerate their progress by unlocking the flow of money and access to services.]")
        st.write(":red[****FEATURES****]")
        st.write("****Simple, Fast & Secure****")
        st.write("****One app for all transactions.****")
        st.write("****Pay whenever you like, wherever you like.****")
        st.write("****Find all your favourite apps on PhonePe Switch.****")
        st.link_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        st.write("     ")
        st.image("https://www.phonepe.com/webstatic/6508/static/bab93065eae063d167f5ea2699093877/c1679/hp-banner-pg.jpg")

elif selected == "Data Exploration":

    tab1,tab2,tab3 = st.tabs(["Aggregaed Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"],key = "1")

        if method == "Insurance Analysis":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y = Transaction_amount_amount_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_amount_Y_Q(tac_Y,quarters)

        elif method == "Transaction Analysis":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y = Transaction_amount_amount_Y(Aggre_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_tran_tac_Y["States"].unique(),key='2')

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_amount_Y_Q(Aggre_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_tran_tac_Y["States"].unique(),key="3")

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

        elif method == "User Analysis":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user,years)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_tran_tac_Y_Q["States"].unique(),key='4')

            Aggre_user_plot_3(Aggre_tran_tac_Y_Q,states)
    
    with tab2:

        method2 = st.radio("Select the Method",["Map Insurance","Map Transaction","Map User"],key = "5")
        if method2 == "Map Insurance":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min(),key="6")
            map_insur_tac_Y = Transaction_amount_amount_Y(map_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_insur_tac_Y["States"].unique(),key='7')

            Map_insur_District(map_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min(),key="23")
            map_insur_tac_Y_Q=Transaction_amount_amount_Y_Q(map_insur_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_insur_tac_Y_Q["States"].unique(),key="376")

            Map_insur_District(map_insur_tac_Y_Q,states)            

        elif method2 == "Map Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min(),key="66")
            map_tran_tac_Y = Transaction_amount_amount_Y(map_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_tran_tac_Y["States"].unique(),key='7')

            Map_insur_District(map_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",map_tran_tac_Y["Quarter"].min(),map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min(),key="23")
            map_tran_tac_Y_Q=Transaction_amount_amount_Y_Q(map_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_tran_tac_Y_Q["States"].unique(),key="3")

            Map_insur_District(map_tran_tac_Y_Q,states)       

        elif method2 == "Map User":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min(),key="45")
            map_user_Y = map_user_plot_1(map_user,years)
            
            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min(),key="53")
            map_user_Y_Q=map_user_plot_2(map_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_user_Y_Q["States"].unique(),key="33")

            map_user_plot_3(map_user_Y_Q,states)

    with tab3:

        method3 = st.radio("Select the Method",["Top Insurance","Top Transaction","Top User"],key = "9")

        if method3 == "Top Insurance":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min(),key="689")
            Top_insur_tac_Y = Transaction_amount_amount_Y(top_insurance,years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Top_insur_tac_Y["States"].unique(),key="34")

            Top_insur_plot_1(Top_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min(),key="24")
            Top_insur_tac_Y_Q=Transaction_amount_amount_Y_Q(Top_insur_tac_Y,quarters)


        elif method3 == "Top Transaction":
        
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min(),key="123")
            Top_tran_tac_Y = Transaction_amount_amount_Y(top_transaction,years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Top_tran_tac_Y["States"].unique(),key="345")

            Top_insur_plot_1(Top_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min(),key="456")
            Top_tran_tac_Y_Q=Transaction_amount_amount_Y_Q(Top_tran_tac_Y,quarters)
            
        
        elif method3 == "Top User":

            col1,col2=st.columns(2)
            with col1:
                years = st.slider("Select the Year",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min(),key="567")
            Top_user_Y = top_user_plot_1(top_user,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Top_user_Y["States"].unique(),key="678")

            top_user_plot_2(Top_user_Y,states)
            
#Top Chart part


def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= map_user[["States", "App_opens"]]
    sa1= sa.groupby("States")["App_opens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "App_opens", title="Top 10 States With AppOpens",
                color_discrete_sequence=['blue'])
    return st.plotly_chart(fig_sa)

def ques6():
    sa= map_user[["States", "App_opens"]]
    sa1= sa.groupby("States")["App_opens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "App_opens", title="lowest 10 States With AppOpens",
                color_discrete_sequence=['blue'])
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

if selected == "Top Charts":

    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()
        
    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()    
