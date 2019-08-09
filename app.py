from flask import Flask, request, jsonify, render_template  # rest api framwork
from flask_sqlalchemy import SQLAlchemy  # db abstraction layer
from flask_marshmallow import Marshmallow  # object serialization
from flask_cors import CORS, cross_origin  # for allowing cors for react ui
import os  # os calls

# init app
app = Flask(__name__, static_folder='templates/static')
CORS(app)


basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize db
db = SQLAlchemy(app)

# initialize marshmallow
ma = Marshmallow(app)

# tasks model


class Task (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)

    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.done = False


# tasks schema
class TaskSchema (ma.Schema):
    class Meta:
        fields = ('id', 'name', 'content', 'done')


# init tasks schema
task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(many=True, strict=True)

# routes and methods

# MAIN


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# USERS


# TASKS
@app.route('/tasks', methods=['POST'])
def add_task():
    name = request.json['name']
    content = request.json['content']
    new_task = Task(name, content)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

# get all
@app.route('/tasks/all', methods=['GET'])
# @cross_origin()
def get_tasks():
    tasks = Task.query.all()
    return tasks_schema.jsonify(tasks)

# get by id
@app.route('/tasks/<id>', methods=['GET'])
def get_task_id(id):
    task = Task.query.filter_by(id=int(id)).first()
    db.session.commit()
    return task_schema.jsonify(task)

# delete all
@app.route('/tasks/all', methods=['DELETE'])
def delete_tasks_all():
    tasks = Task.query.all()
    for task in tasks:
        db.session.delete(task)
    db.session.commit()
    return tasks_schema.jsonify(tasks)

# delete by id
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.filter_by(id=int(id)).first()
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

# update done
@app.route('/tasks/done/<id>', methods=['PUT'])
def update_task_done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return task_schema.jsonify(task)

# update name
@app.route('/tasks/name/<id>', methods=['PUT'])
def update_task_name(id):
    task = Task.query.filter_by(id=int(id)).first()
    name = request.json['name']
    task.name = name
    db.session.commit()
    return task_schema.jsonify(task)

# update content
@app.route('/tasks/content/<id>', methods=['PUT'])
def update_task_content(id):
    task = Task.query.filter_by(id=int(id)).first()
    content = request.json['content']
    task.content = content
    db.session.commit()
    return task_schema.jsonify(task)

# update all done
@app.route('/tasks/done/all', methods=['PUT'])
def update_task_done_all():
    tasks = Task.query.all()
    for task in tasks:
        if request.json['done'].lower() == 'true':
            task.done = True
        else:
            task.done = False
    db.session.commit()
    return tasks_schema.jsonify(tasks)


# run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
