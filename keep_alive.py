import flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Server is alive!"

if __name__ == '__main__':
    app.run(debug=True)
