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

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'GET':
        book_id = request.args.get('book_id')
        if book_id:
            cur.execute("SELECT * FROM reviews WHERE book_id = %s", (book_id,))
        else:
            cur.execute("SELECT * FROM reviews")
        reviews = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'id': r[0], 'book_id': r[1], 'user_id': r[2], 'rating': r[3], 'comment': r[4]} for r in reviews]), 200
    else:
        data = request.json
        book_id = data.get('book_id')
        user_id = data.get('user_id')
        rating = data.get('rating')
        comment = data.get('comment')
        try:
            cur.execute("INSERT INTO reviews (book_id, user_id, rating, comment) VALUES (%s, %s, %s, %s) RETURNING id", 
                        (book_id, user_id, rating, comment))
            review_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Review added', 'review_id': review_id}), 201
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({'message': 'Failed to add review', 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
