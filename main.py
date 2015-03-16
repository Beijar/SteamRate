__author__ = 'patrikpirat & BaraMarcus'

import unirest
from flask import jsonify
#import json
#from urllib import urlopen, quote_plus as urlencode


class Games(object):
    def __init__(self, json):
        self.__score = json['score']
        self.__userScore = json['user_score']
        self.__thumbnail = json['thumbnail']
        self.__title = json['title']
    pass


def api_search(query):
    user_data = get_steam(query)

    for data in user_data:
        print data




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

    game_data = get_metacritic(game_list)

    return game_data

def get_metacritic(list):
    #TO DO: FILTER THE DATA RESULT FOR BETTER EFFICENCY
    game_data = []

    with open('meta_key.txt') as keyfile:
        meta_key = keyfile.read()

    for game in list:
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
            game_data.append(response.body['result']['name'] + response.body['result']['score'])

    print game_data
    return game_data


api_search(76561198042906374)

