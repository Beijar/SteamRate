__author__ = 'PatrikPirat & Marcus'
from flask import Flask, render_template, request, Response, jsonify
import json
from main import api_search, count_average

app = Flask(__name__)


@app.route('/')
def search_js():
    #Main page
    return render_template("search.html")


@app.route('/api/search')
def search_api():
    #API endpoint, takes one argument (Steam ID)
    query = request.args.get('q')

    if not query:
        #if search submit is empty
        return jsonify({'error': 'Bad Request',
                        'code': 400,
                        'message': 'No user ID was provided'
                        }), 400

    try:
        user_game = api_search(query)
        average_score = count_average(user_game)

        return Response(json.dumps({"average":average_score, "result":user_game}, indent=4), status=200, mimetype='application/json')
    except:
        #if SteamRate API has an unexpected error
        return jsonify({'error': 'Internal error',
                        'code': 500,
                        'message': 'Internal server error'
                        }), 500


@app.route('/docs')
def docs():
    #API documentation page
    return render_template("docs.html")


@app.errorhandler(404)
def page_not_found(error):
    if request.path.startswith("/api/"):
        # API requests should get JSON, props to Fredrik!
        return jsonify({ 'error': 'Resource Not Found', 'code': 404, 'message': 'Page does not exist' }), 404
    else:
        # Other requests should get HTML.
        return render_template("error.html", code = 404, description = "Page not found"), 404


if __name__ == '__main__':
    app.debug = True #remove for launch?
    app.run()