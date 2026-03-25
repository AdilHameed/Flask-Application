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
collection2 = db["todo_items"]

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


@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    try:
        item_name = request.form['itemName']
        item_desc = request.form['itemDescription']

        collection2.insert_one({
            "itemName": item_name,
            "itemDescription": item_desc
        })

        return "Item added successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)