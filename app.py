# coding: utf-8
from flask import Flask, render_template, request, Response, jsonify
import json
from main import api_search


app = Flask(__name__)


@app.route('/')
def search_js():
    return render_template("search.html")


@app.route('/api/search')
def search_api():
    query = request.args.get('q')

    if not query:
        return jsonify({'error': 'Bad Request',
                        'code': 400,
                        'message': 'No user ID was provided'
                        }), 400


    user_game = api_search(query)

    return Response(json.dumps({"result":user_game}, indent=4), status=200, mimetype='application/json')

@app.route('/docs')
def docs():
    return render_template("docs.html")


#Kolla på errorhandler senare
'''
@app.errorhandler(404)
def page_not_found(error):
    if request.path.startswith("/api/"):
        # API requests should get JSON
        return jsonify({ 'error': 'Resource Not Found', 'code': 404, 'message': 'Requested endpoint does not exist' }), 404
    else:
        # Other requests should get HTML
        return render_template("error.html", code = 404, description = "Page not found"), 404
'''

if __name__ == '__main__':
    app.debug = True
    app.run()