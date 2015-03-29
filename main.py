__author__ = 'PatrikPirat & Marcus'
'''
Date: 2015-03-29
Description: Mashup API that takes a singel argument as input (a Steam ID).
Extracts user owned games from the Steam API using the ID input then takes those games
and use them as inputs to the unoficiall Metacritic API to extract score data to those games.
Version: First beta version.
'''


import unirest


def api_search(query):
    '''
    Top function that takes the user ID input and calls the Steam & Metacritic API functions.
    When this function gets the return data it filters the result dictionaries in a loop before it returns
    the completed result (sum_gameScore.
    '''
    sum_game_data = []

    user_games = get_steam(query)
    user_scores = get_metacritic(user_games)

    for scores in user_scores:
        del scores['img_logo_url']
        del scores['publisher']
        del scores['summary']
        del scores['platform']
        del scores['appid']
        del scores['img_icon_url']
        sum_game_data.append(scores)

    return sum_game_data

def count_average(game_score):
    '''Function that computes the average user owned gamescore'''
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
    '''
    Function that takes the user ID input and uses it in a GET call to Steam API
    GetOwnedGames. The response is a json file of user owned games. Saves the response as a listed dict and returns it.
    '''
    with open('steam_key.txt', 'r') as f:
        steam_key = f.read()

    response = unirest.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
                           + str(steam_key)
                           + "&steamid=" + str(userID),
                           headers={ "Accept": "application/json" },
                           params={ "include_appinfo": "1", "include_played_free_games": "1" })

    player_data = response.body
    player_games = player_data['response']['games']

    return player_games

def get_metacritic(game_list):
    '''
    The function gets a listed dict of user owned games, response from Steam API call, as argument.
    That argument is looped for calls to Metacritic API, each game titel is saved as a variable from
    the dict and used as param to the Metacriti API call.
    '''
    #TO DO: MULTITHREAD API CALLS
    game_data = []
    gamestuff = game_list[0:10] #Temp. restriction on API calls due to ineffiecency of loop calls.

    with open('meta_key.txt') as keyfile:
        meta_key = keyfile.read()

    for game in gamestuff:
        title = game['name']
        response = unirest.post("https://byroredux-metacritic.p.mashape.com/find/game",
        headers={
        "X-Mashape-Key": str(meta_key),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
        },
        params={
        "platform": 3, #PC
        "retry": 4,
        "title": title
         }
        )

        if response.body['result'] != False:
            game_score = response.body['result']
            combined_data = game.copy()
            combined_data.update(game_score) #combining the game data from Steam API with the Metacritic API response.

            game_data.append(combined_data)

    return game_data