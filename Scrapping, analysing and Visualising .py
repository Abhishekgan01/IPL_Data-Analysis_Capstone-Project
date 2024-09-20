import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

url="https://www.iplt20.com/auction"
r=requests.get(url)

df1 = pd.read_csv("Scrapped Data from top buys in TATA IPL 2024.csv")
print(df1[["TEAM", "PLAYER", "TYPE", "PRICE"]])
print(df1["PRICE"].dtype)
print(df1["PLAYER"].dtype)

# 1. Total Number of Players per Team
players_per_team = df1.groupby("TEAM").size()
print("\nTotal Number of Players per Team:\n", players_per_team)

#2.Funds spends per team
df1["PRICE"] = df1["PRICE"].astype(str)

df1["PRICE"] = df1["PRICE"].str.replace('₹', '').str.replace(",", "").astype(int)
funds_spent_per_team = df1.groupby("TEAM")["PRICE"].sum()
print("\nTotal Funds Spent per Team:\n", funds_spent_per_team)

# 3. Average Price of Players
average_price = df1["PRICE"].mean()
print("\nAverage Price of Players: ₹{:.2f}".format(average_price))

# 4. Total and Average Price by Player Type
pd.options.display.float_format = '{:,.2f}'.format
total_by_type = df1.groupby("TYPE")["PRICE"].sum()
avg_by_type = df1.groupby("TYPE")["PRICE"].mean()
print(total_by_type)
print(avg_by_type)

# 5. Highest and Lowest Priced Player per Team
highest_priced_player = df1.loc[df1.groupby("TEAM")["PRICE"].idxmax()]
lowest_priced_player = df1.loc[df1.groupby("TEAM")["PRICE"].idxmin()]
print(highest_priced_player[["TEAM", "PLAYER", "TYPE", "PRICE"]])
print()
print(lowest_priced_player[["TEAM", "PLAYER", "TYPE", "PRICE"]])

# 6. Team-wise Spend per Player Type
spend_by_team_and_type = df1.groupby(["TEAM", "TYPE"])["PRICE"].sum().unstack()
print("\nTeam-wise Spend per Player Type:\n", spend_by_team_and_type)

spend_by_team_and_type.fillna(0,inplace=True)
spend_by_team_and_type = spend_by_team_and_type.astype(int)
print(spend_by_team_and_type)

players_per_team.plot(kind='bar', title='Total Number of Players per Team', ylabel='Price (₹)')
plt.show()

funds_spent_per_team.plot(kind='bar', title='Total Funds Spent per Team', ylabel='Price (₹)')

funds_spent_per_team.plot(kind='pie', autopct='%1.1f%%', title='Distribution of Funds Spent per Team')

df1["PRICE"] = df1["PRICE"].astype(str) 

df1["PRICE"] = df1["PRICE"].str.replace('₹', '').str.replace(",","").astype(int)
df1["PRICE"].plot(kind='hist', bins=10, title='Distribution of Player Prices', edgecolor='black')
plt.show()

df.plot(kind='scatter', x='TYPE', y='PRICE', title='Price vs Player Type', colorbar="yellow")

highest_priced_player.plot(kind='bar', x='PLAYER', y='PRICE', title='Highest Priced Players per Team')
lowest_priced_player.plot(kind='bar', x='PLAYER', y='PRICE', title='Lowest Priced Players per Team')

fig = px.bar(df, x='TEAM', y='PRICE', title='Total Price by Team', text='PRICE')
fig.show()

fig = px.violin(df, y='PRICE', x='TYPE', title='Price Distribution by Player Type')
fig.show()

df['PRICE'] = df['PRICE'].astype(str)
df['PRICE'] = df['PRICE'].str.replace(',', '').astype(float)
fig = px.scatter_3d(df, x='TEAM', y='TYPE',z='PRICE', color='TYPE', size='PRICE', title='3D View of Player Price by Team and Type')
fig.show()

fig = px.histogram(df, x='PRICE', nbins=10, title='Distribution of Player Prices')
fig.show()

