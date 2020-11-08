from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from . import data_layer as dl


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
@app.route('/players/<query>')

def players(query=None):
    if query==None:
        query="2018"
    players=[]
    res = dataLayer.searchJsonDoc(query)
    for player in res:
        info = dataLayer.getJsonDoc(player['uri'])
        image = dataLayer.getBinaryDoc(info['binary'])
        players.append((info, image))
    print(len(players))
    return render_template('players_list.html', players = players)



@app.route('/search', methods=['POST'])

def search():
    query = request.form['query']
    return redirect((url_for('players', query=query)))



@app.route('/info/<name>')

def info(name=None):
    if not name:
        return redirect(url_for('players'))
    res = dataLayer.searchJsonDoc(name)
    uri=res[0]["uri"]
    info = dataLayer.getJsonDoc(uri)
    image = dataLayer.getBinaryDoc(info['binary'])

    return render_template('learn_more.html', info=info, image=image)



#@app.route('/hello/<name>')
#def hello(name=None):
"""curl --anyauth --user user:password -X GET -i \
-H "Accept: multipart/mixed; boundary=document-part-boundary" \
'tp://localhost:8000/v1/documents?uri=doc1.xml&uri=doc2.json' """