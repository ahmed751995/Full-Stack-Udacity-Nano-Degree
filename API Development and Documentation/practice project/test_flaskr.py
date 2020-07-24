import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db, Book

class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf"
        self.database_path = "postgres:///"+self.database_name
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title': 'Anansi Boys',
            'author': 'Neil Gaiman',
            'rating': 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_newww(self):
        pass

    def test_books(self):
        """Test fetching books"""
        res = self.client().get('/books')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['books']))
        self.assertTrue(data['total_books'])
        
    def test_400_books(self):
        """Test 400 error """
        res = self.client().get('/books?page=1000')
        self.assertEqual(res.status_code, 404)


    def test_books_patch(self):
        """Test patching book """
        res = self.client().patch('/books/1', json={'rating':3})
        data = json.loads(res.data)

        book = Book.query.filter(Book.id == 1).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['rating'], 3)

        
    def test_404_books_patch(self):
        """Test 404 patching book"""
        res = self.client().patch('/books/a', json={'rating':5})
        self.assertEqual(res.status_code, 404)

    def test_400_books_patch(self):
        """Test 404 patching book"""
        res = self.client().patch('/books/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_search_books(self):
        """Test searched books"""
        res = self.client().post('/search', json={'search':'book3'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['books']))
        self.assertTrue(data['total_books'])

    
    def test_404_search_books(self):
        """Test searched books"""
        res = self.client().post('/search', json={'search':'s'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_400_search_books(self):
        """Test searched books"""
        res = self.client().post('/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
