from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration: URLs of the microservices
USER_SERVICE_URL = "http://user-service:5001"
BOOK_SERVICE_URL = "http://book-service:5002"
REVIEW_SERVICE_URL = "http://review-service:5003"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the BookReviewHub Gateway!"}), 200

@app.route('/users/register', methods=['POST'])
def register_user():
    response = requests.post(f"{USER_SERVICE_URL}/register", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/users/login', methods=['POST'])
def login_user():
    response = requests.post(f"{USER_SERVICE_URL}/login", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        response = requests.get(f"{BOOK_SERVICE_URL}/books", params=request.args)
    else:
        response = requests.post(f"{BOOK_SERVICE_URL}/books", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        response = requests.get(f"{REVIEW_SERVICE_URL}/reviews", params=request.args)
    else:
        response = requests.post(f"{REVIEW_SERVICE_URL}/reviews", json=request.json)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
