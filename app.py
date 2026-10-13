
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB.
# Use the environment variable for cloud deployment,
# or the local MongoDB server for local testing.
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# Select the database and collection.
db = client["beginner_db"]
todos_collection = db["todos"]


@app.route("/")
def index():
    # Check whether MongoDB is available.
    client.admin.command("ping")

    # Retrieve all tasks from MongoDB.
    all_todos = list(todos_collection.find())

    return render_template("index.html", todos=all_todos)


@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task", "").strip()

    if task:
        # Insert the submitted task as a document.
        todos_collection.insert_one({"task": task})

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
