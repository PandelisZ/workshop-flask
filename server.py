from flask import Flask, render_template,jsonify, request
import uuid
import json
# I am using redis as my database
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/users', methods=['GET'])
def usersRoute():
    users = []
    userids = r.lrange('userids', 0, -1)
    for key in userids:
        users.append(json.loads(r.get(key)))

    return jsonify(users)


@app.route('/api/users', methods=['POST'])
def usersPostRoute():
    content = request.json
    userid = str(uuid.uuid4())
    content['id'] = userid
    
    r.set(userid, json.dumps(content))
    r.lpush('userids', *[userid])

    return jsonify({
        'status': 'ok',
        'user': {
            'id': userid
        }
    })

@app.route('/api/user/<id>', methods=['GET'])
def usersGetRoute(id):
    return jsonify(json.loads(r.get(id)))

@app.route('/<userName>')
def index(userName):
    user = {'username': userName}
    return render_template('profile.html', title='Home', user=user)

if __name__ == '__main__':
    app.run()
