import xmltodict
import json
import numpy as np
import pandas as pd


# convert xml to json 
def xml2json(xml):

    if xml == None:
        return json.dumps({})

    my_dict = xmltodict.parse(xml)
    json_data=json.dumps(my_dict)

    return json_data

# convert data frame to json record by record 

def df2json(df:pd.DataFrame , path:str):
    df.to_json(path,orient = 'records')


def remove_empty_col(match , col , identifier):
    return match[match[col]!=identifier]

# calculate away team possession
def away_pos(possession:float):
    if (possession == np.NaN):
        return np.NaN
    else:
        return 100 - possession

# calculate home team possession
def extract_pos(possession:str):
    json_object = json.loads(possession)
    try:
        home_pos = json_object['possession']['value'][-1]['homepos']
        return float(home_pos)
    except:
        return np.NaN

# count the number of total shots on target for each team 

def extract_shot(shoton:str, home_team_id:str , away_team_id:str):
    json_object = json.loads(shoton)    
    home_shot_on = 0 
    away_shot_on = 0 
    try:

        for shot in json_object['shoton']['value']:
            if str(shot['team'])==str(home_team_id):
                home_shot_on+=1
            elif str(shot['team'])==str(away_team_id):
                away_shot_on+=1
            
        return [home_shot_on,away_shot_on]

    except:
        return np.NaN,np.NaN

# extract each goal 
def extract_goal(goals:str):
    json_object = json.loads(goals)
    goals = []
    try:            
        for goal in json_object['goal']['value']:

            # find scorer
            if goal.__contains__('player1'):
                scorer = goal['player1']
            else :
                scorer = np.NaN
            
            # find assister
            if goal.__contains__('player2'):
                assister = goal['player2']
            else :
                assister = np.NaN
            
            goals.append((scorer,assister))
        return json.dumps(goals)
    except:
        return json.dumps([])
