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

order_items = db.Table('order_items',
                       db.Column('order_id', db.Integer, db.ForeignKey('order.id'),primary_key=True),
                       db.Column('product_id', db.Integer, db.ForeignKey('product.id'),primary_key=True))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(), nullable=False)
    products = db.relationship('Product', secondary=order_items, backref=db.backref('orders', lazy=True))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<Todo {self.id}  {self.name}>'


    
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}  {self.description}>'

# db.create_all()

@app.route('/list/<listId>/completed', methods=['POST'])
def list_completed(listId):
    try:
        list = TodoList.query.get(listId)
        for todo in list.todos:
            todo.completed = True
            db.session.add(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

        
@app.route('/todos-list/<listId>/delete', methods=['DELETE'])
def delete_list(listId):
    try:
        list = TodoList.query.get(listId)
        for todo in list.todos:
            db.session.delete(todo)
        db.session.delete(list)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos-list/create', methods=['POST'])
def create_list():
    try:
        name = request.get_json()['name']
        print(name)
        todo_list = TodoList(name=name)
        db.session.add(todo_list)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))
        

@app.route('/todos/create', methods=['POST'])
def create():
    error = False
    body = {}

    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, list_id=list_id)
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

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
                           data=Todo.query.filter_by(list_id=list_id).order_by('id').all(),
                           todo_lists=TodoList.query.order_by('id').all(),
                           todo_list=TodoList.query.filter_by(id=list_id).all())



@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=0))
