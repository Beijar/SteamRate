from flask import Flask
#from main import get_steam
import unirest

app = Flask(__name__)


@app.route('/')
def index():
    return ''

@app.route('/search')
def search():
    return 'Hello Marcus'

if __name__ == '__main__':
    app.debug = True
    app.run()
