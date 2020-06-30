from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///example"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<ID: {self.id}, name: {self.name}>'


class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=True)
    issued = db.Column(db.DateTime, nullable=False)
    vehicles = db.relationship('Vehicle', backref='driver', lazy=True)


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(), nullable=False)
    model = db.Column(db.String(), nullable=False)
    year = db.Column(db.DateTime, nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    
db.create_all()

@app.route('/')
def index():
    person = Person.query.first()
    return 'hello ' + person.name

if __name__ == '__main__':
    app.run(debug=True)


    
