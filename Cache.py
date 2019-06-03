from flask import Flask
from flask_cache import Cache
from datetime import datetime

app = Flask(__name__)

cache = Cache(app,config = {'CACHE_TYPE':'simple'})

@app.route('/')
def hello_word():
    return 'HELLO WORLD'

@app.route('/with_cache')
@cache.cached(timeout=5)
def with_cache():
    return str(datetime.utcnow())

if __name__ == '__main__':
    app.run()
