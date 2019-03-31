from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from login import DB, BaseUs, BaseNe
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
conn = db.get_connection()
base = BaseUs(conn)
letters = BaseNe(conn)
base.init_table()
letters.init_table()
mas = ['https://www.youtube.com/embed/jgfTSoScOnU',
       'https://www.youtube.com/embed/lQ6MM6kPImk',
       'https://www.youtube.com/embed/6vp_R0cTQMY',
       'https://www.youtube.com/embed/bPfgUBvKhp0',
       'https://www.youtube.com/embed/5XWtV-zG20Q',
       'https://www.youtube.com/embed/_6HixWtc_sA',
       'https://www.youtube.com/embed/D2vsmXGfIoQ',
       'https://www.youtube.com/embed/SXLcKav2-Bs',
       'https://www.youtube.com/embed/5C4C1GEJPr4',
       'https://www.youtube.com/embed/ipr_XIuedUM',
       'https://www.youtube.com/embed/SxqZj2g8n08',
       'https://www.youtube.com/embed/cQE9INtE8WA',
       'https://www.youtube.com/embed/9r4Duiiw_3g',
       'https://www.youtube.com/embed/FecIvpgyWws',
       'https://www.youtube.com/embed/CZTFWhr90tI',
       'https://www.youtube.com/embed/WpnOFwQBDtM',
       'https://www.youtube.com/embed/Z1OypcvstLs',
       'https://www.youtube.com/embed/NF6nPhvmXCI',
       'https://www.youtube.com/embed/O2IWLorRaQ8',
       'https://www.youtube.com/embed/5spSnvCzTsQ',
       'https://www.youtube.com/embed/oB8KEWQBlOI']
normals = ['gmail.com', 'mail.ru', 'yandex.ru']
cur_name = ''
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global cur_name
    global mas
    if request.method == 'GET':
        return render_template('login.html', add=random.choice(mas))
    elif request.method == 'POST':
        exists = base.exists(request.form['email'], request.form['password'])
        if exists[0]:
            cur_name = request.form['email']
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    global cur_name
    global normals
    global mas
    if request.method == 'GET':
        return render_template('registration.html', add=random.choice(mas))
    elif request.method == 'POST':
        email = request.form['emailreg']
        if email.split('@')[1] in normals:
            base.insert(request.form['emailreg'], request.form['passwordreg'])
            cur_name = request.form['emailreg']
            return redirect(url_for('main'))
        else:
            return redirect(url_for('registration'))

@app.route('/main', methods=['GET', 'POST'])
def main():
    global cur_name
    global mas
    if request.method == 'GET':
        theme = []
        for i in letters.get_all():
            if i[3] == cur_name:
                theme.append(i)
        return render_template('main.html', themes=theme, user=cur_name,
                               add=random.choice(mas))
    elif request.method == 'POST':
        cur_name = ''
        return redirect(url_for('login'))

@app.route('/main/<id>', methods=['POST', 'GET'])
def retid(id):
    global mas
    if request.method == 'GET':
        themes = letters.get(id)
        return render_template('theme.html', id=id, themes=themes,
                               add=random.choice(mas))

@app.route('/sent_letter', methods=['GET', 'POST'])
def add_theme():
    global mas
    if request.method == 'GET':
        return render_template('add_theme.html', add=random.choice(mas))
    elif request.method == 'POST':
        letters.insert(request.form['title'], request.form['text'],
                       request.form['name'])
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')