import os
import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'shopwise.db'),
    SECRET_KEY='development_key'    
))

app.config.from_envvar('PROJECT_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print 'Initialized the database'


def get_db():
   if not hasattr(g, 'sqlite_db'):
     g.sqlite_db = connect_db()
   return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
      g.sqlite_db.close()
  
  
@app.route('/')
def homepage():
    return render_template('homepage.html')
 
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cur = db.cursor()
    db.execute('insert into registered_user(firstname, lastname, username, password) values(?, ?, ?, ?)',[firstname, lastname, username, password])
    db.commit()
    print "Registered!!"
    return render_template('homepage.html')
 
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cur = db.execute('select * from registered_user where username = \
    (?) and password = (?)', [username, password])  
    data = list( cur.fetchone())
    if data is not None:
        session['username'] = data[3]
        session['firstname'] = data[1]
        session['lastname'] = data[2]
        session['id'] = data[0]
        rows = showad()
        return render_template('userHomePage.html', firstname=data[1], lastname=data[2], rows=rows)
    return ""
   
   
@app.route('/postAd',methods=['GET', 'POST'])
def postAd():
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        cur = db.execute('insert into advertisements(title, category, price, name, mobile, email, address, user_id) values(?, ?, ?, ?, ?, ?, ?, ?)',[request.form['title'], request.form['category'], request.form['price'], request.form['name'], request.form['mobile'], request.form['email'], request.form['address'], session['id']])
        db.commit()
        rows=showad()
        return render_template('userHomePage.html',firstname=session['firstname'], lastname=session['lastname'],rows=rows)    
    return render_template('postAd.html')
    

def showad():
    db = get_db()
    cur = db.execute('select id,title,category,price from advertisements where user_id =(?)',[session['id']])
    rows = cur.fetchall()
    print "Inside"
    return rows


@app.route('/editad', methods=['GET', 'POST'])    
@app.route('/editad/<int:ad_id>', methods=['GET', 'POST'])
def editad(ad_id=None):
    if request.method == 'POST': 
        db = get_db()
        cur = db.cursor()
        cur = db.execute('update advertisements set title = (?), category = (?), price = (?),\
        name = (?), mobile = (?), email = (?), address = (?), user_id = (?) where id = (?)',\
        [request.form['title'], request.form['category'], request.form['price'],request.form['name'], request.form['mobile'], request.form['email'],\
        request.form['address'], session['id'], session['ad_id']])
        db.commit()
        print session['ad_id']
        return render_template('userHomePage.html', firstname=session['firstname'], lastname=session['lastname'], rows=showad())
    else:
        db = get_db()
        print ad_id    
        session['ad_id'] = ad_id
        cur = db.execute('select * from advertisements where id = (?)', [session['ad_id']])
        ad_data = cur.fetchone()
    return render_template('postAd.html', ad_data=ad_data)     


@app.route('/delete', methods=['GET'])    
@app.route('/delete/<int:ad_id>', methods=['GET'])
def deleteAd(ad_id=None):
    db = get_db()
    cur = db.cursor()
    db.execute('delete from advertisements where id = (?)', [ad_id])
    db.commit()
    flash("Deleted Successfully!!!! ")
    return render_template('userHomePage.html', firstname=session['firstname'], lastname=session['lastname'], row=showad())
    
    
if __name__ == '__main__':    
    app.run(debug=True, host='127.0.0.1', port=9000)
 

