import hashlib
import json
import os
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()
app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def read_api_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api")
def api():
    return jsonify(read_api_data())


@app.post("/submittodoitem")
def submit_todo_item():
    payload = request.get_json(silent=True) or request.form
    item_name = str(payload.get("itemName", "")).strip()
    item_description = str(payload.get("itemDescription", "")).strip()

    if not item_name or not item_description:
        return jsonify({
            "success": False,
            "error": "Both itemName and itemDescription are required."
        }), 400

    item_id = str(payload.get("itemId") or uuid.uuid4().hex[:8])
    item_uuid = str(payload.get("itemUUID") or uuid.uuid4())
    item_hash = hashlib.sha256(
        f"{item_id}:{item_uuid}:{item_name}:{item_description}".encode("utf-8")
    ).hexdigest()

    document = {
        "itemId": item_id,
        "itemUUID": item_uuid,
        "itemHash": item_hash,
        "itemName": item_name,
        "itemDescription": item_description,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    mongo_uri = os.getenv("MONGODB_URI", "").strip()
    if not mongo_uri:
        return jsonify({
            "success": False,
            "error": "MongoDB is not configured. Set MONGODB_URI in your local .env file.",
            "validatedItem": document
        }), 503

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
        database_name = os.getenv("MONGODB_DATABASE", "git_github_assignment")
        collection = client[database_name]["todo_items"]
        result = collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        client.close()
        return jsonify({"success": True, "message": "To-Do item saved.", "item": document}), 201
    except PyMongoError as exc:
        return jsonify({
            "success": False,
            "error": "Could not save the item to MongoDB. Check your URI and database access.",
            "details": str(exc)
        }), 503


if __name__ == "__main__":
    app.run(debug=True)
