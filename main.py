__author__ = 'patrikpirat & BaraMarcus'

import unirest
import json
#from urllib import urlopen, quote_plus as urlencode


def api_search(query):
    #filter json data
    #name, user-score, metascore, thumbnail
    sum_gameScore = []

    user_games = get_steam(query)
    user_scores = get_metacritic(user_games)

    for scores in user_scores:
        del scores['summary']
        del scores['rating']
        del scores['publisher']
        del scores['platform']
        sum_gameScore.append(scores)

    for sum in sum_gameScore:
        print sum


    return sum_gameScore


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
    #TO DO: DYNAMIC RETURN THE DATA RESULT FOR BETTER EFFICENCY
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


api_search(76561198042906374)

