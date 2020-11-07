from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from . import data_layer as dl
from base64 import b64encode

#from PIL import Image
#from io import BytesIO


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
    resp = dataLayer.getBinaryDoc("/image/MalikBeasley.png")
    #print(r.content) gives hex data
    #pic = Image.open(BytesIO(r.content))
    image = b64encode(resp).decode("utf-8")
    #print(image)

    return render_template('home.html', pic=pic)

@app.route('/players')

def players():
    player = dataLayer.searchJsonDoc("2018")
    print(player)
    """curl --anyauth --user user:password -X GET -i \
    -H "Accept: multipart/mixed; boundary=document-part-boundary" \
    'tp://localhost:8000/v1/documents?uri=doc1.xml&uri=doc2.json' """
    return render_template('players_list.html', players = player)

#@app.route('/hello/<name>')
#def hello(name=None):