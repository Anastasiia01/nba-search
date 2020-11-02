from flask import Flask, render_template
from flask_bootstrap import Bootstrap
#from requests import auth


'''def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app 

app = create_app()'''
app = Flask(__name__)
Bootstrap(app)


if __name__ == "main":
    app.run()

@app.route('/')
#@app.route('/hello/<name>')
#def hello(name=None):
def index():
    return render_template('home.html')

@app.route('/players')
def index():
    return render_template('players.html')

