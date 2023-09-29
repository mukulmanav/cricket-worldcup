#%%
print("hello")
 # %%
import pandas as pd
import json
# %%  reading the json file data of match_result
with open('t20_json_files/t20_wc_match_results.json') as f:
    data=json.load(f)

# %% 
data[0]
# %% converting json data into dataframe

df_match =pd.DataFrame(data[0]['matchSummary'])
df_match

# %%  checking the shape

df_match.shape

# %% renaming the column scorecard to match_id
df_match.rename({'scorecard': 'match_id'},axis=1,inplace=True)
df_match
#%%
match_ids_dict={}

for index,row in df_match.iterrows():
    key1= row['team1'] + ' Vs ' + row['team2']
    key2=row['team2'] + ' Vs ' + row['team1']
    match_ids_dict[key1]=row['match_id']
    match_ids_dict[key2]=row['match_id']
match_ids_dict

#%% converting table into csv file
df_match.to_csv('t20_csv_file/dim_match_summary.csv', index = False)

#%%




# %% reading the json file data of batting_summary
with open('t20_json_files/t20_wc_batting_summary.json') as f:
    data=json.load(f)
data

# %% converting json data into dataframe

all_Records=[]

for rec in data:
    all_Records.extend(rec['battingSummary'])

all_Records

df_batting=pd.DataFrame(all_Records)
# %%   changing dismissal comumn to out/not_out

df_batting['out/not_out']=df_batting.dismissal.apply(lambda x:"out" if len(x) >1 else "Not_out")

# %%
df_batting
# %%
df_batting.drop(columns=['dismissal'],inplace=True)
# %%
df_batting.head(11)
# %% removing special character like  â€ or \xa0

df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace("â€", ''))
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace("\xa0", ''))
df_batting.head()

# %%  making new column match_id

df_batting['match_id']=df_batting['match'].map(match_ids_dict)

# %%
df_batting.head()
# %%
df_batting.to_csv('t20_csv_file/fact_batting_summary.csv',index=False)
# %%



#%%
with open('t20_json_files/t20_wc_bowling_summary.json') as f:
    data=json.load(f)
    
data
# %%
all_Records=[]

for rec in data:
    all_Records.extend(rec['bowlingSummary'])
all_Records

# %%  converting json into dataframe
df_bowling=pd.DataFrame(all_Records)
df_bowling
# %%
df_bowling['match_id']=df_bowling['match'].map(match_ids_dict)
df_bowling.head()
# %%
df_bowling.to_csv('t20_csv_file/fact_bowling_summary.csv', index = False)
# %%





#%% reading json file
with open('t20_json_files/t20_wc_player_info.json') as f:
    data = json.load(f)

data[0]
# %%
df_players=pd.DataFrame(data)
# %% removing weird characters
df_players['name']=df_players['name'].apply(lambda x: x.replace('â€', ''))
df_players['name']=df_players['name'].apply(lambda x: x.replace('†', ''))
df_players['name']=df_players['name'].apply(lambda x: x.replace('\xa0', ''))
df_players.head()

# %%
df_players.to_csv('t20_csv_file/dim_players_no_images.csv', index = False)
# %%
