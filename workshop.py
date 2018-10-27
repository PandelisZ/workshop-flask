from flask import Flask, request, jsonify, render_template
import json
import uuid
from random import *
# I am using redis as my database
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/user', methods=['POST'])
def userCreateRoute():
    incoming = request.json

    userid = str(uuid.uuid4())
    incoming['id'] = userid

    r.set(userid, json.dumps(incoming))
    r.lpush('knownids', *[userid])

    return jsonify(incoming)

@app.route('/api/user/<userid>', methods=['GET'])
def userGetRoute(userid):

    if r.exists(userid):
        user = json.loads(r.get(userid))

        return jsonify(user)

    else:
        return jsonify({
            'status': 'Not found'
        }) 

@app.route('/api/users', methods=['GET'])
def usersGetAllRoute():
    knownids = r.lrange('knownids', 0,-1)
    allusers = []
    for id in knownids:
        allusers.append(json.loads(r.get(id)))

    return jsonify(allusers)

@app.route('/api/user/random', methods=['GET'])
def usersGetRandomRoute():
    knownids = r.lrange('knownids', 0,-1)
    idIndex = randint(0, len(knownids))

    return jsonify(json.loads(r.get(knownids[idIndex])))

@app.route('/user/<userid>')
def userView(userid):

    if r.exists(userid):
        user = json.loads(r.get(userid))

        return render_template('userprofile.html', user=user)
    else:
        return render_template('userprofile.html', user={'name': 'unknown', 'address': ''})



if __name__ == '__main__':
    app.run() # create the webserver
