# coding=utf-8
from flask import Flask, render_template, Markup, flash, redirect, url_for
import os


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'SIT')


user = {
    'username': 'Dabao Guo',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/')
@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/index')
def index():
    return render_template('index.html')


# 自定义上下文
@app.context_processor
def inject_info():
    foo = 'i am foo'
    return dict({'foo': foo})


# 自定义全局函数
@app.template_global()
def bar():
    return 'I am bar'


# 自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835')


# 自定义过滤器
@app.template_test()
def is_year(year):
    if str(year) == '1994':
        return True
    else:
        return False


# flash
@app.route("/flash")
def just_flash():
    flash("你好，我是flash, 你是谁?")
    return redirect(url_for('index'))


# 错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404
