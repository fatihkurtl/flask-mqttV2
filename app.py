# yarım bırakma 
import email
from flask import *
import sqlite3
import json
from h11 import Data #
import pandas as pd
import requests
import flask_login
####
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
import email_validator
####

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'dooplabs'

#### ContactForm Database Start
class contactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(granular_message=True)])
    message = StringField(label='Message')
    submit = SubmitField(label="Send")
#### ContactForm Database End

def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

@app.route('/')
def index():
    return render_template('login.html')

# login page
user = {"username": "admin", "password": "admin123"} #

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:

            session['user'] = username
            return redirect('/view')
        
        return "<h1>Wrong username or password</h1>"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


@app.route('/view')
def dashboard():
    if 'user' in session and session['user'] == user['username']:
        con = sqlite3.connect('mqtt.db')
        con.row_factory = row_to_dict
        cur = con.cursor()
        cur.execute("SELECT * FROM raspberry_data")
        rows = cur.fetchall()
        return render_template("view.html", rows = rows)
    
    # return  '<h1>You are not logged in.</h1>'

# @app.route('/logout')
# def logout():
#     session.pop('user')
#     return redirect('/login')

# main app
# @app.route("/view")
# def view():
#     con = sqlite3.connect('mqtt.db')
#     con.row_factory = row_to_dict
#     cur = con.cursor()
#     cur.execute("SELECT * FROM raspberry_data")
#     rows = cur.fetchall()
#     return render_template("view.html", rows = rows)

@app.route("/topic")
def topic():
    con = sqlite3.connect("mqtt.db")
    con.row_factory = row_to_dict
    cur = con.cursor()
    cur.execute("SELECT id, topic, time FROM raspberry_data")
    rows = cur.fetchall()
    return render_template("topic.html", rows = rows)

@app.route("/payload")
def payload():
    con = sqlite3.connect("mqtt.db")
    con.row_factory = row_to_dict
    cur = con.cursor()
    cur.execute("SELECT id, payload, time FROM raspberry_data")
    rows = cur.fetchall()
    return render_template("payload.html", rows = rows)



@app.route("/contact", methods=["GET", "POST"])
def home():
    cform=contactForm()
    if cform.validate_on_submit():
            print(f"Name:{cform.name.data}, E-mail:{cform.email.data}, message:{cform.message.data}")
    return render_template("contact.html",form=cform)






# @app.route("/model")
# def model():
#     con = sqlite3.connect("mqtt.db")
#     con.row_factory = row_to_dict
#     cur = con.cursor()
#     cur.execute("SELECT id FROM raspberry_data")
#     rows = cur.fetchall()
#     print(rows)
#     return render_template("model.html", rows = rows)

# @app.route("/") # hometemp database'e bağlı
# def view():
#     con = sqlite3.connect("mqtt.db")
#     con.row_factory = row_to_dict
#     cur = con.cursor()
#     cur.execute("SELECT * FROM hometemp")
#     wors = cur.fetchall()
#     return render_template("index.html", wors = wors)


# @app.route('/model')
# def model():
#     con = sqlite3.connect("mqtt.db")
#     db = pd.read_sql_query("SELECT * FROM raspberry_data", con)
#     url = db
   
#     return jsonify(url)






#     conn = sqlite3.connect('mqtt.db')
#     data = pd.read_sql_query("SELECT * FROM raspberry_data", conn)
#     i = int(data)
#     for x in i:
#         print(x['id'])
#     return render_template('model.html')

    
    

    # url = 'http://127.0.0.1:5000/'
    # x = json.loads(url)
    # return jsonify(x['id'])

# @app.route("/model")
# def model():
#     if(request.method == 'GET'):

#         url = 'http://127.0.0.1:5000'
#         return jsonify(url['payload'])

    # api_url = "http://127.0.0.1:5000/"
    # response = requests.get(api_url['payload'])
    # response.json()
    # return render_template('model.html') 



# @app.route('/post', methods = ['POST'])
# def post():
#     id = request.form['id']
#     topic = request.form['topic']
#     payload = request.form['payload']
#     created_at = request.form['created_at']
#     print(id, topic, payload, created_at)
#     return redirect(url_for('/'))


# @app.route("/mqttList", methods=['POST', 'GET'])
# def mqttList():
#     try:
#         if request.method == 'POST':   
#             id = request.form.get['id']
#             topic = request.form.get['topic']
#             payload = request.form.get['payload']
#             create_at = request.form.get['create_at']

#             with sqlite3.connect('mqtt.db') as database:
#                 database.row_factory = sqlite3.Row

#                 cursor = database.cursor()
#                 cursor.execute("SELECT * FROM raspberyy_data")
#                 rows = cursor.fetchall()

#             return render_template("list.html", rows = rows)

#     except:
#         return render_template("index.html", hata = "hata oluştu")


if __name__ == '__main__':
   app.run(debug = True, port=4321, host="0.0.0.0")