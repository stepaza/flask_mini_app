from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
import os

################################################################################################################
###  Code for flask app.py
################################################################################################################

app = Flask(__name__)

################################################################################################################
###  Setup the "Database"
################################################################################################################

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

################################################################################################################
###  Setup Authentication
################################################################################################################
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

################################################################################################################
###  GET Methods
################################################################################################################
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required

def get_task(task_id):
    # print(task_id) # For testing purposes
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
################################################################################################################
###  POST Methods
################################################################################################################
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required

def create_task():
    # print(request.json) # For testing purposes
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    # Write task to file
    task_nbr = task['id']
    with open(os.path.join(os.environ['TASK_PATH'], str(task_nbr) + '.txt'), 'w') as taskfile:
        taskfile.write(f"id = {task['id']}\n")
        taskfile.write(f"title = {task['title']}\n")
        taskfile.write(f"Description = {task['description']}\n")
        taskfile.write(f"Done = {task['done']}\n")
    return jsonify({'task': task}), 201

################################################################################################################
###  DELETE Methods
################################################################################################################
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required

def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id] # this list will always be of length 1
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    # Delete the task file if it exists
    try:
        os.remove(os.path.join(os.environ['TASK_PATH'], 'T' + str(task[0]['id'])  + '.txt'))
    except Exception as e:
        nothing = ''
    return jsonify({'result': True, 'Message from the API' : 'Successfully deleted task ' + str(task_id)})

################################################################################################################
###  PUT Methods
################################################################################################################
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required

def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    # if 'title' in request.json and type(request.json['title']) != unicode: # unicode testing currently not implemented (is it really necessary? >> default encoding for python 3)
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0], 'Message from the API' : 'Successfully updated task ' + str(task_id)})

################################################################################################################
###  Global Error Handling
################################################################################################################
@app.errorhandler(404) # improve the error handler, as ERROR 404 returns an HTML string by default from Flask

def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')

