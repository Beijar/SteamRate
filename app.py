from flask import Flask, request, jsonify
from main import search_api
import unirest

app = Flask(__name__)


@app.route('/api/v1/search')
def index():
    query = request.args.get('q')

    # No movie title was provided
    if not query:
        # Return an error and set an appropriate status code
        return jsonify({'error': 'Bad Request',
                        'code': 400,
                        'message': 'No movie title was provided'
                        }), 400
    pass

@app.route('/search')
def search():
    return 'Hello Marcus'

if __name__ == '__main__':
    app.debug = True
    app.run()
