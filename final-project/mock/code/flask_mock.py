import json
import random

from flask import Flask, jsonify, request
import settings

app = Flask(__name__)

MOCK_DATA = {}


@app.route('/', methods=['GET'])
def get_root():
    return 'Okay'


@app.route('/vk_id/<username>', methods=['GET'])
def get_id(username):
    if username in MOCK_DATA:
        vk_id = MOCK_DATA[username]
        return jsonify({'vk_id': str(vk_id)}), 200
    else:
        return jsonify({}), 404


@app.route('/vk_id/add_user', methods=['POST'])
def add_user():
    user_name = json.loads(request.data)['name']
    value = json.loads(request.data)['value']
    if user_name not in MOCK_DATA:
        MOCK_DATA[user_name] = value
        return jsonify({'id': MOCK_DATA[user_name]}), 201
    else:
        return jsonify(f'User {user_name} already have vk_id'), 400


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify(f'OK, exiting'), 200


if __name__ == '__main__':
    app.run(host=settings.MOCK_HOST, port=settings.MOCK_PORT)

