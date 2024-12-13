from flask import Flask, render_template, url_for, request, flash, session, redirect, abort,g,make_response
# from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import datetime
from FDataBase import FDataBase
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))
app.config['SECRET_KEY'] = '55bd0e5eafba522af51c798b496bb6b09d2b1097'
menu = ["Главная страница","Страница о нас","Регистрцаия","Вход"]

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db
@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()
@app.route("/main" ,methods=["POST", "GET"])
def main():

    return render_template('main.html', title='Главная страница', text='main',menu=menu)

@app.route("/register" ,methods=["POST", "GET"])
def register():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        print(request.form['name'])
        print(url_for('register'))

    return render_template('register.html', title='Регистрация', text='main',menu=dbase.getMenu())

@app.route("/login" ,methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('login.html', title='Вход', text='main',menu=dbase.getMenu())

@app.route("/about" ,methods=["POST", "GET"])
def about():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('about.html', title='О нас', text='main',menu=dbase.getMenu())


if __name__ == "__main__":

    app.run(debug=True)
