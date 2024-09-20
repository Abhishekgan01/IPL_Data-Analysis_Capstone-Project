import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

st.title("Welcome to IPL Analysis")
st.snow()

df = pd.read_csv("Scrapped Data from top buys in TATA IPL 2024.csv")

url = "https://www.iplt20.com/auction"
r = requests.get(url)

df1 = pd.read_csv("Scrapped Data from top buys in TATA IPL 2024.csv")
st.write(df1[["TEAM", "PLAYER", "TYPE", "PRICE"]])
st.write(df1["PRICE"].dtype)
st.write(df1["PLAYER"].dtype)

# 1. Total Number of Players per Team
players_per_team = df1.groupby("TEAM").size()
st.write("\nTotal Number of Players per Team:\n", players_per_team)

# 2. Funds spent per team
df1["PRICE"] = df1["PRICE"].astype(str)
df1["PRICE"] = df1["PRICE"].str.replace('₹', '').str.replace(",", "").astype(int)
funds_spent_per_team = df1.groupby("TEAM")["PRICE"].sum()
st.write("\nTotal Funds Spent per Team:\n", funds_spent_per_team)

# 3. Average Price of Players
average_price = df1["PRICE"].mean()
st.write("\nAverage Price of Players: ₹{:.2f}".format(average_price))
print()

# 4. Total and Average Price by Player Type
pd.options.display.float_format = '{:,.2f}'.format
total_by_type = df1.groupby("TYPE")["PRICE"].sum()
avg_by_type = df1.groupby("TYPE")["PRICE"].mean()
st.write("\nTotal Price of Players in each type",total_by_type)
st.write("\nAverage Price of Players in each type",avg_by_type)

# 5. Highest and Lowest Priced Player per Team
highest_priced_player = df1.loc[df1.groupby("TEAM")["PRICE"].idxmax()]
lowest_priced_player = df1.loc[df1.groupby("TEAM")["PRICE"].idxmin()]
st.write("Highest Priced Player in each team",highest_priced_player[["TEAM", "PLAYER", "TYPE", "PRICE"]])
st.write("Second highest Priced Player in each team",lowest_priced_player[["TEAM", "PLAYER", "TYPE", "PRICE"]])

# 6. Team-wise Spend per Player Type
spend_by_team_and_type = df1.groupby(["TEAM", "TYPE"])["PRICE"].sum().unstack()
st.write("\nTeam-wise Spend per Player Type:\n", spend_by_team_and_type)

st.write("###Replacing NAN with 0")
spend_by_team_and_type.fillna(0, inplace=True)
spend_by_team_and_type = spend_by_team_and_type.astype(int)
st.write(spend_by_team_and_type)

# Plot visualizations in Streamlit
# 1. Bar plot for Total Number of Players per Team
st.write("### Total Number of Players per Team")
fig, ax = plt.subplots()
players_per_team.plot(kind='bar', title='Total Number of Players per Team', ax=ax)
st.pyplot(fig)

# 2. Bar plot for Total Funds Spent per Team
st.write("### Total Funds Spent per Team")
fig, ax = plt.subplots()
funds_spent_per_team.plot(kind='bar', title='Total Funds Spent per Team', ax=ax)
st.pyplot(fig)

# 3. Pie chart for Funds Distribution per Team
st.write("### Distribution of Funds Spent per Team")
fig, ax = plt.subplots()
funds_spent_per_team.plot(kind='pie', autopct='%1.1f%%', title='Distribution of Funds Spent per Team', ax=ax)
st.pyplot(fig)

# 4. Histogram for Player Price Distribution
st.write("### Distribution of Player Prices")
fig, ax = plt.subplots()
df1["PRICE"].plot(kind='hist', bins=10, title='Distribution of Player Prices', edgecolor='black', ax=ax)
st.pyplot(fig)

# 5. Scatter plot: Price vs Player Type
st.write("### Price vs Player Type")
fig = px.scatter(df, x='TYPE', y='PRICE', title='Price vs Player Type')
st.plotly_chart(fig)

# 6. Bar plot for Highest and Lowest Priced Players per Team
st.write("### Highest Priced Players per Team")
fig = px.bar(highest_priced_player, x='PLAYER', y='PRICE', title='Highest Priced Players per Team')
st.plotly_chart(fig)

st.write("### Lowest Priced Players per Team")
fig = px.bar(lowest_priced_player, x='PLAYER', y='PRICE', title='Lowest Priced Players per Team')
st.plotly_chart(fig)

# 7. Bar plot for Total Price by Team
st.write("### Total Price by Team")
fig = px.bar(df, x='TEAM', y='PRICE', title='Total Price by Team', text='PRICE')
st.plotly_chart(fig)

# 8. Violin plot for Price Distribution by Player Type
st.write("### Price Distribution by Player Type")
fig = px.violin(df, y='PRICE', x='TYPE', title='Price Distribution by Player Type')
st.plotly_chart(fig)

# 9. 3D Scatter plot for Player Price by Team and Type
st.write("### 3D View of Player Price by Team and Type")

# Ensure PRICE is numerical for scatter plot
df['PRICE'] = df['PRICE'].str.replace(',', '').astype(float)

fig = px.scatter_3d(df, x='TEAM', y='TYPE', z='PRICE', color='TYPE', size='PRICE', title='3D View of Player Price by Team and Type')
st.plotly_chart(fig)

# 10. Histogram for Player Price Distribution
st.write("### Player Price Distribution")
fig = px.histogram(df, x='PRICE', nbins=10, title='Distribution of Player Prices')
st.plotly_chart(fig)
