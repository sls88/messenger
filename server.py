import time
from datetime import datetime as dt
from flask import Flask, request
import re

app = Flask(__name__)
db = []


@app.route("/")
def hello():
    return "Добро пожаловать на сервер нашего Мессенджера! <a href='/status'>Статус</a>"


@app.route("/status")
def status():
    dn = dt.now()
    return {
        'users': len(set(i['name'] for i in db)),
        'messages': len(db),
        'status': True,
        'name': 'Messenger',
        'time': dn.strftime('%d.%m.%Y %H:%M:%S')
    }


@app.route("/send", methods=['POST'])
def send():
    data = request.json
    s = data['text']
    b = "Текст содержит запрещенные слова!"
    correct = re.sub(r".*жопа.*|.*какашка.*|.*кролик.*", b, s)
    if correct != b:
        db.append({
            'id': len(db),
            'name': data['name'],
            'text': data['text'],
            'timestamp': dt.now().timestamp()
        })
        return {'ok': True}
    else:
        return {'ok': b}


@app.route("/messages")
def messages():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_timestamp'])
    else:
        after_timestamp = 0

    after_id = 0
    for i in db:
        if i['timestamp'] <= after_timestamp:
            after_id += 1
        else:
            break
    return {'messages': db[after_id:after_id+100]}

app.run()
