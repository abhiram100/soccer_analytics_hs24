import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import json

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
df_penalty = pd.DataFrame()
for index, row in team_df.iterrows():
    id = row['wyscout']
    f_name = str(id) + '.json'
    df_ev = wyscout_json_to_df(f_name)
    df_pen = df_ev[(df_ev['type.primary']=='penalty')&(df_ev['team.name']== team)]
    df_penalty = pd.concat([df_penalty,df_pen],ignore_index=True)

print(df_penalty)

pitch = Pitch(pitch_color='white', line_color='black')
fig, ax = pitch.draw(figsize=(10, 7))

for index, row in df_free_kick .iterrows():
    x = row['location.x']
    y = row['location.y']
    dx = row['pass.endLocation.x'] - x
    dy = row['pass.endLocation.y'] - y
    # change length and proportions
    # you get data with a field which is 100x100 and you want to plot it in a field with 120x80
    x = nx(x)
    y = ny(y)
    dx = nx(dx)
    dy = ny(dy)

    
    # set the arrow_color depending on the startpoint of the free kick - change "80"
    if x >= 80:
        arrow_color = 'green'
    else:
        arrow_color = 'orange'
        continue

    passCircle=plt.Circle((x,y),2,color=arrow_color)
    passCircle.set_alpha(.2)
    ax.add_patch(passCircle)

    passArrow = plt.Arrow(x, y, dx, dy, width=2, color=arrow_color)
    ax.add_patch(passArrow)
    
passLine = plt.plot([80,80],[0,80],linewidth=3,color='red') # line marking the attacking third
ax.set_title(f"{team}'s freekicks 2023", fontsize=24) # change title
fig.set_size_inches(10, 7)

plt.show()
