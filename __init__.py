from flask import Flask, render_template

app = Flask(__name__)

@app.route('/happy')
def welcome():
    return 'Welcome to Jobifly!'

if __name__ == "main":
    app.run()