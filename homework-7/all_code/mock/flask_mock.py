import json
import threading

from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

SURNAME_DATA = {}


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return jsonify(surname), 200
    else:
        return jsonify(f'Surname for user {name} not found'), 404


@app.route('/add_surname', methods=['POST'])
def add_user_surname():
    user_name = json.loads(request.data)['name']
    user_surname = json.loads(request.data)['surname']
    if user_name not in SURNAME_DATA:
        SURNAME_DATA[user_name] = user_surname
        data = {user_name: user_surname}
        return jsonify(data), 201
    else:
        return jsonify(f'User surname {user_name} already exists: if you want update surname, go to /update_surname'), 400


@app.route('/update_surname/<user_name>', methods=['PUT'])
def update_user_surname(user_name):
    user_surname = json.loads(request.data)['surname']
    if user_name in SURNAME_DATA:
        SURNAME_DATA[user_name] = user_surname
        data = {user_name: user_surname}
        return jsonify(data), 201   # Здесь поправить
    else:
        return jsonify(f'User {user_name} and his surname {user_surname} are not exists: if you want add surname, go to /add_surname'), 400


@app.route('/delete_surname/<user_name>', methods=['DELETE'])
def delete_user_surname(user_name):
    if user_name in SURNAME_DATA:
        surname = SURNAME_DATA.pop(user_name)
        data = {user_name: surname}
        return jsonify(data), 204
    else:
        return jsonify(f'User {user_name} is not exist'), 400


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify(f'OK, exiting'), 200
