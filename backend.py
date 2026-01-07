import os
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from frontend import Frontend

class Backend:
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name][collection_name]

    def get_items(self) -> list[dict]:
        projection = {"_id": 0, "id": 1, "fullName": 1, "email": 1, "type": 1, "discount": 1, "totalSale": 1}
        docs = list(self.collection.find({}, projection).sort("fullName", 1))
        return docs

def create_app() -> Flask:
    mongo_uri = os.getenv(
        "MONGO_URI",
        "mongodb+srv://oop:oop@cluster0.9knxc.mongodb.net/oop?retryWrites=true&w=majority&appName=Cluster0",
    )
    db_name = os.getenv("MONGO_DB", "oop")
    collection_name = os.getenv("MONGO_COLLECTION", "Customers")

    backend = Backend(mongo_uri, db_name, collection_name)
    frontend = Frontend()
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def index():
        items = backend.get_items()
        return frontend.render(items)

    @app.route("/api/items")
    def api_items():
        return jsonify(backend.get_items())

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", "4010")))
