from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///todoapp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}  {self.description}'

db.create_all()

@app.route('/')
def index():
    return render_template('index.html',data=db.session.query(Todo).all())