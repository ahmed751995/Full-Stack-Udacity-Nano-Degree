from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from .models import setup_db, Book

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allowed-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allowed-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    @app.route('/books')
    def hello():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 2
        end = start + 2
        books = Book.query.all()
        formatted_books = [book.format() for book in books]
        
        return jsonify({
            'success': True,
            'books': formatted_books[start:end],
            'total-books': len(formatted_books)})

    @app.route('/books/<int:book_id>')
    def get_specific_book(book_id):
        book = Book.query.filter(Book.id == book_id).one_or_none()
        if book == None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'book': book.format()
            })
    
        
    return app
