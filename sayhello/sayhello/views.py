from flask import flash, render_template, redirect, url_for

from sayhello import app, db
from sayhello.models import Message
from sayhello.forms import HelloForm


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        m = Message(name=name, body=body)
        db.session.add(m)
        db.session.commit()
        flash("Your Message have been saved!")
        redirect(url_for('index'))
    # return render_template('index.html', form=form, messages=messages)
    return render_template('index_bootstrap.html', form=form, messages=messages)
