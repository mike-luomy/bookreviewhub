from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configuration
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'database')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'bookreviewhub')
DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'postgres')

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DATABASE_HOST,
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD
    )
    return conn

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'GET':
        search = request.args.get('search')
        if search:
            cur.execute("SELECT * FROM books WHERE title ILIKE %s OR author ILIKE %s", 
                        (f"%{search}%", f"%{search}%"))
        else:
            cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'id': b[0], 'title': b[1], 'author': b[2], 'genre': b[3], 'publication_date': b[4].strftime('%Y-%m-%d')} for b in books]), 200
    else:
        data = request.json
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        publication_date = data.get('publication_date')
        try:
            cur.execute("INSERT INTO books (title, author, genre, publication_date) VALUES (%s, %s, %s, %s) RETURNING id", 
                        (title, author, genre, publication_date))
            book_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Book added', 'book_id': book_id}), 201
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({'message': 'Failed to add book', 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
