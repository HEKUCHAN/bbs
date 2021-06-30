from flask import Flask, render_template, request
from models.models import Message
from models.database import db_session
from datetime import datetime

app = Flask(__name__)

@app.template_filter('seigen')
def seigen_filter(s):
    return str(s)[:30]

@app.template_filter('cutDate')
def cut_date(date):
    return str(date).split('.')[0]

@app.template_filter('reverse')
def reverse(string):
    return string[::-1]

@app.route("/")
def index():
    messages = Message.query.all()
    return render_template("index.html", messages = messages)

@app.route('/new')
def new():
    return render_template("new.html")

@app.route('/edit/<int:id>')
def edit(id):
    post = Message.query.get(id)
    return render_template('edit.html', message = post)


@app.route('/update/<int:id>', methods=['POST'])
def update_post(id):
    post = Message.query.filter_by(id=id).first()
    post.title = request.form['u-title']
    post.body = request.form['u-content']
    post.date = datetime.now()
    db_session.commit()

    return render_template('show.html', message = post)

@app.route("/posts/<int:id>")
def show(id):
    content = Message.query.get(id)
    return render_template("show.html",message = content)

@app.route("/delete/<int:id>")
def delete(id):
    content = Message.query.get(id)
    db_session.delete(content)
    db_session.commit()

    message = Message.query.all()

    return render_template("index.html", messages = message)


@app.route('/create', methods=['POST'])
def create():
    new_box = Message()
    new_box.title = request.form['title']
    new_box.body = request.form['content']

    db_session.add(new_box)
    db_session.commit()

    message = Message.query.get(new_box.id)

    return render_template('show.html', message = message)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
