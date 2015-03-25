__author__ = 'patrikpirat & BaraMarcus'

import unirest


def api_search(query):
    sum_gameScore = []

    user_games = get_steam(query)
    user_scores = get_metacritic(user_games)

    for scores in user_scores:
        del scores['summary']
        del scores['rating']
        del scores['publisher']
        del scores['platform']
        sum_gameScore.append(scores)

    return sum_gameScore

def count_average(game_score):
    total_score = 0
    count = 0

    for score in game_score:
        userscore = score['userscore']

        if userscore != None:
            total_score += userscore
            count += 1

    average = total_score/count
    average_result = round(average, 1)

    return average_result

def get_steam(userID):
    with open('steam_key.txt', 'r') as f:
        steam_key = f.read()

    game_list = []
    response = unirest.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
                           + str(steam_key)
                           + "&steamid=" + str(userID),
                           headers={ "Accept": "application/json" },
                           params={ "include_appinfo": "1", "include_played_free_games": "1" })

    player_data = response.body
    player_games = player_data['response']['games']

    for game in player_games:
        game_list.append(game['name'])

    return game_list

def get_metacritic(game_list):
    #TO DO: MULTITHREAD API CALLS
    game_data = []
    gamestuff = game_list[0:10]

    with open('meta_key.txt') as keyfile:
        meta_key = keyfile.read()

    for game in gamestuff:
        response = unirest.post("https://byroredux-metacritic.p.mashape.com/find/game",
        headers={
        "X-Mashape-Key": str(meta_key),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
        },
        params={
        "platform": 3, #PC
        "retry": 4,
        "title": game
         }
        )

        if response.body['result'] != False:
            game_score = response.body['result']
            game_data.append(game_score)

    return game_data