from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load env variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["test_db"]
collection = db["students"]

# 1. API Route
@app.route('/api')
def get_data():
    with open('data.json') as f:
        data = json.load(f)
    return jsonify(data)

# 2. Form Page
@app.route('/')
def form():
    return render_template('form.html')

# Handle Form Submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        age = int(request.form['age'])

        collection.insert_one({"name": name, "age": age})

        return redirect(url_for('success'))
    except Exception as e:
        return render_template('form.html', error=str(e))

# Success Page
@app.route('/success')
def success():
    return render_template('success.html')


# 3. To-Do List Page
@app.route('/todo')
def todo():
    return render_template('todo.html')

if __name__ == '__main__':
    app.run(debug=True)