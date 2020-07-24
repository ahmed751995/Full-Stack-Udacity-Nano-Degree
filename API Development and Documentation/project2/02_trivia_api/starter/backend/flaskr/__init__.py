#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formated_questions = [question.format() for question in questions]

    return formated_questions[start:end]


def formating_categories(categories):
    formated_categories = {}

    for category in categories:
        fcategory = category.format()
        formated_categories[fcategory['id']] = fcategory['type']

    return formated_categories


def create_app(test_config=None):

  # create and configure the app

    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        return response

    @app.route('/categories')
    def categories():
        try:
            categories = Category.query.all()

            formated_categories = formating_categories(categories)

            return jsonify({'success': True,
                            'categories': formated_categories})
        except Exception:

            abort(400)

    @app.route('/questions')
    def questions():
        try:
            categories = Category.query.all()
            questions = Question.query.all()

            formated_categories = formating_categories(categories)
            current_questions = paginate_questions(request, questions)

            if len(
                    current_questions) == 0:       # ensure that a proper page number is used in request args
                raise

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': formated_categories,
                'current_category': None,
            })
        except Exception:

            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id
                                             == question_id).one_or_none()
            question_id = question.id

            if question is None:       # ensure that he entered proper id
                raise

            question.delete()

            return jsonify({
                'success': True,
                'id': question_id
            })
        except BaseException:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def post_question():

        try:
            body = request.get_json()
            search = body.get('searchTerm')

            if search:
                if len(search) == 0:
                    raise

                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search))).all()

                current_questions = paginate_questions(request,
                                                       questions)
                categories = Category.query.all()
                current_category = {}

                for q in questions:
                    if q.category not in current_category:
                        cat_type = Category.query.filter(
                            Category.id == q.category).one_or_none().type
                        current_category[q.category] = cat_type

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questions),
                    'current_category': current_category,
                })
            else:

                if 'question' not in body or 'answer' not in body \
                        or 'difficulty' not in body or 'category' \
                        not in body:  # ensure that all question attributes are submitted
                    raise

                question = Question(question=body.get('question'),
                                    answer=body.get('answer'),
                                    difficulty=body.get('difficulty'),
                                    category=body.get('category'))
                question.insert()

                return jsonify({
                    'success': True,
                    'id': question.id
                })
        except Exception:

            abort(400)

    @app.route('/categories/<int:id>/questions')
    def category_questions(id):

        try:
            current_category = Category.query.filter(Category.id
                                                     == id).one_or_none()

            if current_category is None:
                raise

            questions = Question.query.filter(Question.category
                                              == id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category': current_category.id,
            })
        except Exception:

            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            body = request.get_json()
            categories = body.get('quiz_category')
            previousQuestions = body.get('previous_questions')

            if categories['id'] == 0:
                questions = Question.query.all()
            else:

                questions = Question.query.filter(Question.category
                                                  == categories['id']).all()

            formated_questions = [q.format() for q in questions]

            if len(previousQuestions) == len(formated_questions):
                return jsonify({'success': True})

            while True:
                rand_question = random.choice(
                    formated_questions)  # generate random question
                found = True
                for q in previousQuestions:
                    if q == rand_question['id']:
                        found = False
                        break
                if found:
                    return jsonify({'success': True,
                                    'question': rand_question})
        except Exception:

            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({'success': False, 'error': 404,
                         'message': 'resource not found'}), 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({'success': False, 'error': 422,
                         'message': 'unprocessable'}), 422)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({'success': False, 'error': 400,
                         'message': 'bad request'}), 400)

    @app.errorhandler(500)
    def bad_request(error):
        return (jsonify({'success': False, 'error': 500,
                         'message': 'internal server error'}), 500)
    return app
