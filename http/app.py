from flask import Flask, request, redirect, url_for, jsonify, make_response, session, abort
import os
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'SIT')


# @app.route('/')
# @app.route('/hello', methods=['GET'])
# def hello():
#     name = request.args.get('name')
#     if name is None:
#         name = request.cookies.get('name', 'wangwu')
#     return '<h1>Hello, %s!</h1>' % name


# get name value from query string and cookie
@app.route('/')
@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'zhangsan')
    response = '<h1>Hello, %s!</h1>' % name
    # return different response according to the user's authentication status
    if 'login_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


# use int URL converter
@app.route('/goback/<int:year>', methods=['GET'])
def go_back(year):
    return '<h1>Welcome to %d !</h1>' % (2019 - year)


# redirect
@app.route('/hi', methods=['GET'])
def hi():
    return redirect(url_for('hello'))


# 404
@app.route('/404')
def not_found():
    abort(404)


# return json
@app.route('/foo', methods=['GET'])
def foo():
    return jsonify({"name": 'li si', 'gender': 'male'})


# set cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


# login
@app.route('/login')
def login():
    session['login_in'] = True
    return redirect(url_for('hello'))


# protect view
@app.route('/admin')
def admin():
    if 'login_in' not in session:
        abort(403)
    return 'Welcome to admin page'


# logout
@app.route('/logout')
def logout():
    if 'login_in' in session:
        session.pop('login_in')
    return redirect(url_for('hello'))


# return to last page
@app.route('/foo1')
def foo1():
    return '<h1><Foo1 Page/h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1><Bar Page/h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)


@app.route('/do_something')
def do_something():
    return redirect_back()


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# ajax
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
    <h1> A very long post </h1>
    <div class="body">%s</div>
    <button id="load">Load More </button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function(){
       $('#load').click(function() {
          $.ajax({
            url: '/more',
            type: 'get',
            success: function(data) {
                $('.body').append(data);
            }
          })
       })
    })
    </script>''' % post_body


@app.route('/more')
def load_more():
    return generate_lorem_ipsum(n=1)
