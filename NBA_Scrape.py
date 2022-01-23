from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

# NBA season we will be analyzing
year = 2021
# URL page we will scraping (see image above)
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
# this is the HTML from the given URL
html = urlopen(url)
soup = BeautifulSoup(html)

sal_url = "https://www.basketball-reference.com/contracts/players.html"#.format(year)
sal_html = urlopen(sal_url)
sal_soup = BeautifulSoup(sal_html)

# use findALL() to get the column headers
soup.findAll('tr', limit=2)
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:]

sal_soup.findAll('tr', limit=2)
sal_headers = [th.getText() for th in sal_soup.findAll('tr', limit=2)[1].findAll('th')]
sal_headers = sal_headers[1:]

# avoid the first header row
rows = soup.findAll('tr')[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

sal_rows = sal_soup.findAll('tr')[2:]
player_sals = [[td.getText() for td in sal_rows[i].findAll('td')]
            for i in range(len(sal_rows))]

#Inspect DF of stats
stats = pd.DataFrame(player_stats, columns = headers)
salaries = pd.DataFrame(player_sals, columns = sal_headers)

stats = stats.dropna()
stats= stats.reset_index(drop=True)

salaries = salaries.dropna()
salaries= salaries.reset_index(drop=True)
salaries['2021-22']= pd.to_numeric(salaries['2021-22'].replace('[^0-9\.-]', '',regex = True)).fillna(0)
salaries['2022-23']= pd.to_numeric(salaries['2022-23'].replace('[^0-9\.-]', '',regex = True)).fillna(0)
salaries['2023-24']= pd.to_numeric(salaries['2023-24'].replace('[^0-9\.-]', '',regex = True)).fillna(0)
salaries['2024-25']= pd.to_numeric(salaries['2024-25'].replace('[^0-9\.-]', '',regex = True)).fillna(0)
salaries['2025-26']= pd.to_numeric(salaries['2025-26'].replace('[^0-9\.-]', '',regex = True)).fillna(0)
salaries['2026-27']= pd.to_numeric(salaries['2026-27'].replace('[^0-9\.-]', '',regex = True)).fillna(0)
salaries['Guaranteed']= pd.to_numeric(salaries['Guaranteed'].replace('[^0-9\.-]', '',regex = True)).fillna(0)


#Join DFs
combined = stats.merge(salaries, left_on='Player', right_on='Player')

#Correct Names
combined['Player'] = combined['Player'].str.split(' ').str[::-1].str.join(', ')

#Output todays updated stats into csv
today = date.today()
d1 = today.strftime("%m_%d_%Y")
filename = d1 + "_NBA_Stats.csv"
#print(filename)
combined.to_csv(filename)