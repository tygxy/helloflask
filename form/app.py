import os
import uuid

from flask import Flask, render_template, flash, redirect, url_for, session, send_from_directory, request

from forms import LoginForm, FortyTwoForm, UploadForm, UploadForms, NewPostForm, SigninForm, RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home %s' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


#   自定义验证器
@app.route('/validation', methods=['GET', 'POST'])
def validation():
    form = FortyTwoForm()
    if form.validate_on_submit():
        answer = form.answer.data
        flash('answer is %d' % answer)
        return redirect(url_for('index'))
    return render_template('validation.html', form=form)


#   上传单文件
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success!')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/show_images')
def show_images():
    return render_template('uploaded.html')


#  上传多文件
@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    form = UploadForms()
    if form.validate_on_submit():
        filenames = []
        num = 0
        for f in request.files.getlist('photos'):
            filename = random_filename(f.filename)
            filenames.append(filename)
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            num += 1
        flash('Upload %d file success!' % num)
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('uploads.html', form=form)


#  单个表单多个提交按钮
@app.route('/two-submits', methods=['GET', 'POST'])
def two_submit():
    form = NewPostForm()
    if form.validate_on_submit():
        if form.save.data:
            flash("You click the save button.")
        elif form.publish.data:
            flash('You click the publis button')
        return redirect(url_for('index'))
    return render_template('2submit.html', form=form)


#  单个页面多个表单----单视图处理
@app.route('/multi-form', methods=['GET', 'POST'])
def multi_form():
    signin_form = SigninForm()
    register_form = RegisterForm()

    if signin_form.submit1.data and signin_form.validate_on_submit():
        username = signin_form.username.data
        flash('%s, you just submit sign in button' % username)
        return redirect(url_for('index'))

    if register_form.submit2.data and register_form.validate_on_submit():
        username = signin_form.username.data
        flash('%s, you just submit register button' % username)
        return redirect(url_for('index'))

    return render_template('2form.html', signin_form=signin_form, register_form=register_form)


#  单个页面多个表单----多视图处理
@app.route('/multi-form-multi-view')
def multi_form_multi_view():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)


@app.route('/handle-signin', methods=['POST'])
def handle_signin():
    signin_form = SigninForm2()
    register_form = RegisterForm2()

    if signin_form.validate_on_submit():
        username = signin_form.username.data
        flash('%s, you just submit sign in button' % username)
        return redirect(url_for('index'))

    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)


@app.route('/handle-register', methods=['POST'])
def handle_register():
    signin_form = SigninForm2()
    register_form = RegisterForm2()

    if register_form.validate_on_submit():
        username = register_form.username.data
        flash('%s, you just submit register button' % username)
        return redirect(url_for('index'))

    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)
