from flask import *

app = Flask(__name__)

@app.route('/api/hello') #API routing endpoint
def home():
    return "Hello Fucking World!!!"

app.run(port=5000)
