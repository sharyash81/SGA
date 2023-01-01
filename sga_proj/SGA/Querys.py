import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
database = client['SGA']


# num of games in a season
def num_games(name, season, side = 'home'):
    if side != 'home':
        side = 'away'
    numGame = list(database['Match'].aggregate([
        {'$match':
            {f'{side}_team_api_id': int(database['Team'].find_one(
                {'team_long_name': name})['team_api_id']),
            'season' : f"{season}/{season+1}"}},
        {'$count': 'num_ofGame'}
        ]))
    return numGame[0]['num_ofGame']


# sum goals of a team (define home/away)
def home_away_goal(name, season, side='home'):
    if side != 'home':
        side = 'away'
    num_goal= list(database['Match'].aggregate([
        {'$match':
            {f'{side}_team_api_id': int(database['Team'].find_one(
                {'team_long_name': name})['team_api_id']),
            'season' : f"{season}/{season+1}"}},
        {'$group':
            {'_id' : f'${side}_team_api_id',
            f'{name}\'s {side} goal': {'$sum': f'${side}_team_goal'}}
        }
    ]))
    for team in num_goal:
        print(team)
    return num_goal[0][f'{name}\'s {side} goal']
    

def total_goal(name, season):
    totalGoal = home_away_goal(name, season) + home_away_goal(name, season, 'away')
    print(totalGoal)
    return totalGoal

#     average position of a team (define home/away)



def home_away_pos(name, season, side='home'):
    if side != 'home':
        side = 'away'
    num_pos= list(database['Match'].aggregate([
        {'$match':
            {f'{side}_team_api_id': int(database['Team'].find_one(
                {'team_long_name': name})['team_api_id']),
            'season' : f"{season}/{season+1}"}},
        {'$group':
            {'_id': f'${side}_team_api_id',
            f'{name}\'s {side} pos': {'$avg' : f'${side}_pos'}
        }},
        {'$project':
            {f'{name}\'s {side} pos':
                {'$round' : [f'${name}\'s {side} pos', 2]}}
        }
    ]))
    for team in num_pos:
        print(team)
    return num_pos[0][f'{name}\'s {side} pos']



def total_pos(name, season):
    homePos = home_away_pos(name, season)
    awayPos = home_away_pos(name, season, 'away')
    totalPos = homePos*num_games(name, season) + awayPos*num_games(name, season, 'away')
    totalPos /= num_games(name, season) + num_games(name, season, 'away')
    totalPos = round(totalPos,2)
    print(totalPos)
    return totalPos

#  number of result(win lose draw ,define type type)
def num_result(team_name, season, type = 'd'):
    # type 'w' for win, type 'l' for lose
    check_home = '$eq'
    check_away = '$eq'
    if type == 'w':
        check_home = '$lt'
        check_away = '$gt'
    if type == 'l':
        check_home = '$gt'
        check_away = '$lt'
    num_lose = list(database['Match'].aggregate([
        {'$match':
            {'$or' : [
                { '$and':[
                {f'home_team_api_id': int(database['Team'].find_one(
                    {'team_long_name': team_name})['team_api_id']),
                'season': f"{season}/{season+1}"},
                {'$expr': {check_home : ['away_team_goal', 'home_team_goal']}}]
                },
                { '$and':[
                {f'away_team_api_id': int(database['Team'].find_one(
                    {'team_long_name': team_name})['team_api_id']),
                'season': f"{season}/{season+1}"},
                {'$expr': {check_away : ['away_team_goal', 'home_team_goal']}}]
                },
                ]}},
        {'$count': 'num_ofLose'}
    ]))
    if len(num_lose) == 0:
        print(0)
        return 0
    print(num_lose[0]['num_ofLose'])
    return num_lose[0]['num_ofLose']
#  draw in a season 
# num_result("FC Barcelona", 2009)
#  win in a season 
# num_result("FC Barcelona", 2009, 'w')
#  lost in a season 
# num_result("FC Barcelona", 2009, 'l')

###############################

# game history of 2 club
# num of game
def headTohead_game(home_name, away_name):
    num_game= list(database['Match'].aggregate([
        {'$match':
            {f'home_team_api_id': int(database['Team'].find_one(
                {'team_long_name': home_name})['team_api_id']),
            f'away_team_api_id': int(database['Team'].find_one(
                {'team_long_name': away_name})['team_api_id'])}},
        {'$count': "num_ofGame"}]))
    print(num_game[0]['num_ofGame'])
    return num_game[0]['num_ofGame']
        
        
def total_headTohead_game(club1, club2):
    club1_id = int(database['Team'].find_one({'team_long_name': club1})['team_api_id'])
    club2_id = int(database['Team'].find_one({'team_long_name': club2})['team_api_id'])
    num_game = list(database['Match'].aggregate([
        {'$match':
                {'$or' : [
                    {f'home_team_api_id': club1_id,
                    f'away_team_api_id': club2_id},
                    {f'home_team_api_id': club2_id,
                    f'away_team_api_id': club1_id}
                ]}
                },
        {'$count': "num_ofGame"}]))
    if len(num_game) == 0:
        print(0)
        return 0
    print(num_game[0]['num_ofGame'])
    return num_game[0]['num_ofGame']

# goal of home and away(return home goals, away goals)
def headTohead_goal(home_name, away_name):
    num_goal= list(database['Match'].aggregate([
        {'$match':
            {f'home_team_api_id': int(database['Team'].find_one(
                {'team_long_name': home_name})['team_api_id']),
            f'away_team_api_id': int(database['Team'].find_one(
                {'team_long_name': away_name})['team_api_id'])}},
        {'$group':
            {'_id' : f'',
            f'{home_name}\'s home goal': {'$sum': f'$home_team_goal'},
            f'{away_name}\'s away goal': {'$sum': f'$away_team_goal'}}
        }
    ]))
    for team in num_goal:
        print(team)
    return num_goal[0][f'{home_name}\'s home goal'], num_goal[0][f'{away_name}\'s away goal']
# total goals (2 club)
def headTohead_totalGoal(club1, club2):
    club1_home = headTohead_goal(club1, club2)
    club2_home = headTohead_goal(club2, club1)
    total_club1 = club1_home[0]+club2_home[1]
    total_club2 = club1_home[1]+club2_home[0]
    print(total_club1,total_club2)
    return total_club1, total_club2

def headTohead_draw(club1, club2):
    club1_id = int(database['Team'].find_one({'team_long_name': club1})['team_api_id'])
    club2_id = int(database['Team'].find_one({'team_long_name': club2})['team_api_id'])
    num_draw = list(database['Match'].aggregate([
        {'$match':
            {'$and': [
                {'$or' : [
                    {f'home_team_api_id': club1_id,
                    f'away_team_api_id': club2_id},
                    {f'home_team_api_id': club2_id,
                    f'away_team_api_id': club1_id}
                ]},
                {'$expr': {'$eq': ['$away_team_goal','$home_team_goal']}}]
            }
        },
        {'$count': "num_ofGame"}]))
    if len(num_draw) == 0:
        print(0)
        return 0
    print(num_draw[0]['num_ofGame'])
    return num_draw[0]['num_ofGame']


def headTohead_win1(club1, club2):
    club1_id = int(database['Team'].find_one({'team_long_name': club1})['team_api_id'])
    club2_id = int(database['Team'].find_one({'team_long_name': club2})['team_api_id'])
    num_draw = list(database['Match'].aggregate([
        {'$match':
            {'$or': [
                {'$and' : [
                    {f'home_team_api_id': club1_id,
                    f'away_team_api_id': club2_id},
                    {'$expr': {'$lt': ['$away_team_goal','$home_team_goal']}}]
                },
                {'$and' : [
                    {f'home_team_api_id': club2_id,
                    f'away_team_api_id': club1_id},
                    {'$expr': {'$gt': ['$away_team_goal','$home_team_goal']}}]
                }
                ]},
        },
        {'$count': "num_ofGame"}]))
    if len(num_draw) == 0:
        print(0)
        return 0
    print(num_draw[0]['num_ofGame'])
    return num_draw[0]['num_ofGame']


##########################################

# players functions

def num_goal(player_name):
    player_id = str(database['Player'].find_one({'player_name': player_name})['player_api_id'])
    # player_numGoal = list(database['Match'].aggregate([
    #     {'$match': 
    #         {'goals': {'$elemMatch': {'$elemMatch': [player_id]}}}
    #         },
    #     {'$count': 'num_ofGoals'}
    # ]))
    mr_goal = database['Match'].find({'goals': {'$elemMatch': {'$elemMatch': [player_id]}}})
    print(mr_goal)
    # if len(player_numGoal) == 0:
    #     print(0)
    #     return 0
    # print(player_numGoal[0]['num_ofGoal'])
    # return player_numGoal[0]['num_ofGoal']

num_goal('Lionel Messi')
# def num_assist(player_name):


# goal_season
# assist_season
# goal_toTeam
# assist_toTeam
# max_goalSeason
# max_assistSeason
# max_assist_toTeam
# max_goal_toTeam








# home_away_goal("FC Barcelona", 'away')
# home_away_goal("FC Barcelona")
# total_pos("FC Barcelona",2008)
# total_goal("FC Barcelona",2008)
# headTohead_draw("Newcastle United", "Stoke City")
# total_headTohead_game("Newcastle United", "Stoke City")
# headTohead_goal("Real Madrid CF", "FC Barcelona")
# headTohead_draw("Real Madrid CF", "FC Barcelona")
# headTohead_win1("FC Barcelona", "Real Madrid CF")

# headTohead_totalGoal("Real Madrid CF", "FC Barcelona")
# home_away_pos("FC Barcelona", 'home')