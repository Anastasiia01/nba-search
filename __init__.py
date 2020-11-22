from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from .data_layer import DataLayer
import requests
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c6f0cc646e644b15d920872d4d2756d480e455f447124405'
app.config['DEBUG'] = True
Bootstrap(app)
dataLayer = DataLayer()


if __name__ == "main":
    app.run()

@app.route('/')
def index():
    return render_template('home.html')


@app.route("/logout")
def logout():
    """Logout the current user."""
    # Remove 'username' from the session if it exists
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        given = request.form['password']
        uri="/user/{}.json".format(username)
        try:
            res = dataLayer.getJsonDoc(uri)
            pas=res['password']
            if check_password(pas, given):
                session['username'] = username   # Save in session
                return redirect(url_for('index'))
            else:
                #wrong password
                return render_template('login.html', wrong_credentials=True)
        except requests.exceptions.RequestException:
            #wrong username
            return render_template('login.html', wrong_credentials=True)
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        given = request.form['password']
        uri="/user/{}.json".format(username)
        try:
            res = dataLayer.getJsonDoc(uri)
            return render_template('sign_up.html', user_exists = True)
        except:
            enc_pass = generate_password_hash(given)
            data={}
            data["username"]=username
            data["password"]=enc_pass
            dataLayer.putJsonDoc(uri, data, "user")
            return render_template('home.html')
    return render_template('sign_up.html')


@app.route("/profile", methods=['GET', 'POST'])
def profile():   
    if request.method == 'POST':
        return render_template('profile.html', change=True)
    return render_template('profile.html')


@app.route('/change', methods=['POST'])
def change():
    data = {"pathlang": "jsonpath", "patch": [{"replace" : {"select": "password"}}]}
    username = session['username']
    oldpass = request.form['oldpass']
    newpass = request.form['newpass']
    uri="/user/{}.json".format(username)
    try:
        res = dataLayer.getJsonDoc(uri)
        pas=res['password']
        if check_password(pas, oldpass):
            #update pass in MarkLogic
            data["patch"][0]["replace"]["content"]=generate_password_hash(newpass)
            dataLayer.patchJsonDoc(uri, data)

            return render_template('profile.html', updated=True)
        else:
            return render_template('profile.html', change=True, wrong_pass=True)
    except:
        return render_template('home.html')


@app.route('/players')
@app.route('/players/<query>')

def players(query=None):
    if 'username' not in session:
        return redirect(url_for('login'))
    if query==None:
        query="2018"
    players=[]
    res = dataLayer.searchJsonDoc(query)
    for player in res:
        info = dataLayer.getJsonDoc(player['uri'])
        image = dataLayer.getBinaryDoc(info['binary'])
        players.append((info, image))
    return render_template('players_list.html', players = players)

def check_password(actual, given):
    """Check hashed password."""
    return check_password_hash(actual, given)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    return redirect((url_for('players', query=query)))


@app.route('/info/<name>')
def info(name=None):
    if 'username' not in session:
        return redirect(url_for('login'))
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