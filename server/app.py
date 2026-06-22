#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/articles/<int:id>')
def show_article(id):

    # 1. Initialize session counter
    if 'page_views' not in session:
        session['page_views'] = 0

    # 2. Increment on every request
    session['page_views'] += 1

    # 3. Enforce paywall (after 3 views)
    if session['page_views'] > 3:
        return {
            "message": "Maximum pageview limit reached"
        }, 401

    # 4. Fetch article
    article = Article.query.get(id)

    if not article:
        return {"error": "Article not found"}, 404

    # 5. Return article data
    return make_response(ArticleSchema().dump(article), 200)


if __name__ == '__main__':
    app.run(port=5555)
