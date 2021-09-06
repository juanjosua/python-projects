import requests, bs4
import pandas as pd

hero = 'slark'
url = 'https://www.dotabuff.com/heroes/{}/items'.format(hero)

result = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'})
soup = bs4.BeautifulSoup(result.text, "html.parser")

table = soup.find_all('table', {'class': 'sortable'})

# turn the soup into a dataframe
df = pd.read_html(str(table))[0]

# rename the columns
df.columns = ['null', 'item_name', 'match_played', 'win_rate']

# drop the first column
df.drop('null', axis='columns', inplace=True) 

# remove % fron the win_rate and change the type to float
df['win_rate'] = df['win_rate'].str.replace('%', '')
df['win_rate'] = df['win_rate'].astype(float)

df.to_csv('{}_items.csv'.format(hero))

# data cleaning
mp_median = df['match_played'].median()
wr_median = df['win_rate'].median()
df_new = df.loc[df['match_played'] > mp_median]

# print(df_new.info()) # meta data of the dataframe
# print(df_new.sort_values('win_rate', ascending=False).head(10))
# print(df_new.sort_values('match_played', ascending=False).head(10))

# get the top 10 items based on best match_played and best win_rate
n = 50
mp_lrgst = df['match_played'].nlargest(n)
wr_lrgst = df['win_rate'].nlargest(n)

top_10 = df.query('match_played in @mp_lrgst & win_rate in @wr_lrgst')
print(', '.join(top_10["item_name"].values))
