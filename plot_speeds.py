import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import json
import scipy.spatial as spatial
from math import isnan
import numpy as np

# This function reads the wyscout_eventdata (JSON file) and converts it to a
# pandas DataFrame
def wyscout_json_to_df(file_name):
    with open(base_path+ '/' +file_name, encoding='utf8') as f:
        js = json.load(f)
        df = pd.json_normalize(js['events'])
    return df

# these functions changes the points according to the length and width of the field
# see more informations below

def nx(x):
    return x/100*120
def ny(y):
    return y/100*80

path_matchids = './matchids.csv' # replace * by your path to matchids.csv
base_path = './input/wyscout' # replace * by your path
team = 'Hungary' # replace * by your team
data = pd.read_csv(path_matchids)
team_df = data[(data['home']== team)|(data['away']== team)]

#dataframe with all corners of all games from your team
df_success_pass = pd.DataFrame()
df_fail_pass = pd.DataFrame()
df_goals = pd.DataFrame()

bins = np.linspace(0, 90, 10)

SUCCESS_PASS = []
FAIL_PASS = []

for index, row in team_df.iterrows():
    success_pass = np.zeros(10)
    fail_pass = np.zeros(10)
    id = row['wyscout']
    f_name = str(id) + '.json'
    df_ev = wyscout_json_to_df(f_name)
    
    _df_success_pass = df_ev[(df_ev['type.primary']=='pass')&(df_ev['team.name']== team)&(~pd.isnull(df_ev['pass.accurate']&df_ev['pass.accurate']))]
    _df_goals = df_ev[~pd.isnull(df_ev['possession.attack.withGoal']) & (df_ev['possession.attack.withGoal'])]
    
    df_success_pass = pd.concat([df_success_pass,_df_success_pass],ignore_index=True)
    df_goals = pd.concat([df_goals,_df_goals],ignore_index=True)
    
    
    # count
    goal_for = 0
    goal_for_times = []
    goal_against = 0
    goal_against_times = []
    for i in range(len(df_goals)):
        if df_goals.iloc[i]['team.name'] == team:
            goal_for_times.append(df_goals.iloc[i]['minute'])
        else:
            goal_against_times.append(df_goals.iloc[i]['minute'])
    
    
    goal_for_times = list(set(goal_for_times))
    goal_against_times = list(set(goal_against_times))
    score_for = len(goal_for_times)
    score_against = len(goal_against_times)
            
    
    print("Goals for: ", score_for)
    print("Goals against: ", score_against)
    print("Goal times for: ", goal_for_times)
    print("Goal times against: ", goal_against_times)
    
    for i in range(len(df_success_pass)):
        idx = int(df_success_pass['minute'][i]/10)
        if df_success_pass['pass.accurate'][i]:
            success_pass[idx] += 1
        else:
            fail_pass[idx] += 1
    
    # print("Success pass: ", success_pass)
    # print("Fail pass: ", fail_pass)
    
    SUCCESS_PASS.append(success_pass)
    FAIL_PASS.append(fail_pass)
    
    
    df_success_pass = pd.DataFrame()
    df_fail_pass = pd.DataFrame()
    df_goals = pd.DataFrame()

suc = np.zeros(10)
fail = np.zeros(10)
for i in range(len(SUCCESS_PASS)):
    suc += SUCCESS_PASS[i] / np.sum(SUCCESS_PASS[i]+FAIL_PASS[i])
    fail += FAIL_PASS[i] / np.sum(SUCCESS_PASS[i]+FAIL_PASS[i])

plt.figure(figsize=(15, 8))
plt.bar(bins-2, suc, alpha=0.5, label='Success Pass', width=3.5, color='green')
plt.bar(bins+2, fail, alpha=0.5, label='Fail Pass', width=3.5, color='red')
plt.xticks(bins)
plt.title('HUN Success and Fail Passes over a game')
plt.xlabel('Minutes')
plt.ylabel('Number of passes')
plt.legend()
plt.show()
    
    


