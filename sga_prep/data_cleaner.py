import pandas as pd
from utils import * 
import json
import os

def player_feature_selection(player_json_path,player_attr_json_path):

    # read player json file 
    player = pd.read_json(player_json_path)
    player = player[["player_api_id","player_name","birthday","height","weight"]]

    # read player_attr json file 
    player_attr = pd.read_json(player_attr_json_path)
    player_attr = player_attr[["player_api_id","date","preferred_foot"]]

    # result player collection
    result_player = pd.merge(player,player_attr[['player_api_id','date','preferred_foot']],on='player_api_id',how='left')
    print("+++++ Player collection created successfully +++++")

    # convert result_player df to json 
    os.system("rm -rf jsonCols/Player.json jsonCols/Player_Attributes.json")
    os.system("touch jsonCols/Player.json")
    df2json(result_player, "jsonCols/Player.json")
    print("+++++ player collection convert to json successfully +++++")


def match_feature_selection(match_json_path):

    # read match json file
    match = pd.read_json(match_json_path)
    # fields that are xml 
    xml_cols = ['shoton' , 'possession', 'goal']
    for col in xml_cols:
        match[[col]] = match[[col]].apply(lambda x: xml2json(x[col]), axis = 1, result_type='broadcast')
    for col in xml_cols:
        match = remove_empty_col(match, col,'{}')


    # extract goals by each player from xml
    match['goals'] = match[['goal','home_team_api_id','away_team_api_id']].apply(lambda x : extract_goal(x['goal'],x['home_team_api_id'],x['away_team_api_id']), axis=1 , result_type='expand')
    # extract shots on target from xml
    match[['home_shoton','away_shoton']] = match[['shoton','home_team_api_id','away_team_api_id']].apply(
        lambda x : extract_shot(x['shoton'],x['home_team_api_id'],x['away_team_api_id']), axis=1 , result_type='expand')

    # extract the posession of each team from xml 
    match['home_pos'] = match[['possession']].apply(lambda x: extract_pos(x['possession']), axis=1 ,result_type='broadcast')
    match['away_pos'] = match['home_pos'].apply(lambda x: away_pos(x))

    # remove empty fields
    possible_nan_cols = ['home_pos','away_pos','home_shoton','away_shoton']
    possible_empty_cols = ['goals']

    # remove possible NaN columns 
    for col in possible_nan_cols:
        match = remove_empty_col(match, col, np.NaN)

    # remove possible empty columns
    for col in possible_empty_cols:
        match = remove_empty_col(match, col, json.dumps([]))
    # result match collection
    result_match = match[['match_api_id','home_team_api_id','away_team_api_id','season','date',
    'country_id','league_id','home_team_goal','away_team_goal','home_shoton','away_shoton','home_pos','away_pos','goals']]
    print("+++++ Match collection created successfully +++++ ")

    # convert result_match df to json 
    os.system("rm -rf jsonCols/Match.json")
    os.system("touch jsonCols/Match.json")
    df2json(result_match, "jsonCols/Match.json") 
    print("+++++ Match collection convert to json successfully +++++ ")


# feature selection and data cleaning 
if __name__ == '__main__':
    print("***** Data cleaning process starts *****") 
    # clean player feature 
    player_feature_selection("jsonCols/Player.json","jsonCols/Player_Attributes.json")

    # clean match feauture
    match_feature_selection("jsonCols/Match.json")
    print("***** Data cleaned Successfully")



