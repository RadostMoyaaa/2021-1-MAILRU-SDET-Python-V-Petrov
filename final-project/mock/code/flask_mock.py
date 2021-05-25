import random

from flask import Flask, jsonify, request
import settings

app = Flask(__name__)

MOCK_DATA = {}

user_id_seq = 1


@app.route('/', methods=['GET'])
def get_root():
    return jsonify('yxadi'), 400


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_surname(username):
    vk_id = random.randint(0, 100)
    return jsonify({'vk_id': vk_id}), 200


# @app.route('/vk_id/<username>', methods=['GET'])
# def get_user_surname(username):
#     if username in MOCK_DATA:
#         vk_id = random.randint(0, 100)
#         return jsonify({'vk_id': vk_id}), 200
#     else:
#         return jsonify('User doesn't exist'), 404


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

