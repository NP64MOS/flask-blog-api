from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')

@app.route('/api/articles', methods=['POST'])
def add_article():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (title, content))
    return jsonify({'message': 'Article added'}), 201

@app.route('/api/articles', methods=['GET'])
def get_articles():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.execute("SELECT id, title FROM articles ORDER BY id DESC")
        articles = [{'id': row[0], 'title': row[1]} for row in cursor.fetchall()]
    return jsonify(articles)

@app.route('/api/articles/<int:id>', methods=['GET'])
def get_article(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.execute("SELECT title, content FROM articles WHERE id=?", (id,))
        row = cursor.fetchone()
        if row:
            return jsonify({'title': row[0], 'content': row[1]})
        return jsonify({'message': 'Not found'}), 404

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True)

init_db()