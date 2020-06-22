from flask import Flask, render_template, \
    request, redirect, url_for, jsonify, abort

from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///todoapp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id}  {self.description}>'

# db.create_all()

@app.route('/todos/create', methods=['POST'])
def create():
    error = False
    body = {}

    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
        body['id'] = todo.id;
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:  
        db.session.close()
    if error:
        abort (400)
    else:
        return jsonify(body)

@app.route('/todos/<todoId>/set-completed', methods=['POST'])
def set_completed_todo(todoId):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todoId)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todoId>/delete', methods=['DELETE'])
def delete_todo(todoId):
    try:
        todo = Todo.query.get(todoId)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

@app.route('/')
def index():
    return render_template('index.html',data=db.session.query(Todo).order_by('id').all())
