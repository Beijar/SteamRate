# coding: utf-8
from flask import Flask, request, jsonify
from main import api_search
import unirest

app = Flask(__name__)


@app.route('/api/search')
def index():
    query = request.args.get('q')


    if not query:

        return jsonify({'error': 'Bad Request',
                        'code': 400,
                        'message': 'No user ID was provided'
                        }), 400
    pass

    user_game = search_api(query)
    return json.dumps(apidata)




#Kolla på errorhandler senare
"""
@app.errorhandler(404)
def page_not_found(error):
    if request.path.startswith("/api/"):
        # API requests should get JSON
        return jsonify({ 'error': 'Resource Not Found', 'code': 404, 'message': 'Requested endpoint does not exist' }), 404
    else:
        # Other requests should get HTML
        return render_template("error.html", code = 404, description = "Page not found"), 404



if __name__ == '__main__':
    app.debug = True
    app.run()
"""