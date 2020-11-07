from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from . import data_layer as dl


'''def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app
app = create_app()'''
app = Flask(__name__)
Bootstrap(app)
dataLayer = dl.DataLayer()


if __name__ == "main":
    app.run()


@app.route('/')

def index():
    image = dataLayer.getBinaryDoc("/image/MalikBeasley.png")
    return render_template('home.html', image=image)

@app.route('/players')

def players():

    players=[]
    res = dataLayer.searchJsonDoc("2018")
    for player in res:
        info = dataLayer.getJsonDoc(player['uri'])
        image = dataLayer.getBinaryDoc(info['binary'])
        players.append((info, image))
    players=players[0:3]
    print(len(players))
    return render_template('players_list.html', players = players)

@app.route('/search')

def search():
    #result = dataLayer.getJsonDocs('/player/KyleAnderson.json&uri=/player/MoBamba.json&category=content')
    #print(result.json())
    return "<html><p>res</p></html>"

#@app.route('/hello/<name>')
#def hello(name=None):
"""curl --anyauth --user user:password -X GET -i \
-H "Accept: multipart/mixed; boundary=document-part-boundary" \
'tp://localhost:8000/v1/documents?uri=doc1.xml&uri=doc2.json' """