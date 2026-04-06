from flask import Flask, request, jsonify
from pymongo import MongoClient, WriteConcern, ReadPreference

app = Flask(__name__)

CONNECTION_STRING = "mongodb+srv://dbUser:dbUserPassword@cluster0.wvrubl6.mongodb.net/?appName=Cluster0"
DB_NAME = "ev_db"
COLLECTION_NAME = "vehicles"

client = MongoClient(CONNECTION_STRING)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# 1. Fast but Unsafe Write
@app.route(“/insert-fast”, methods=[“POST”])
def insert_fast():
    data = request.json
    coll_fast = collection.with_options(write_concern=WriteConcern(w=1))
    result = coll_fast.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

# 2. Highly Durable Write
@app.route(“/insert-safe”, methods=[“POST”])
def insert_safe():
    data = request.json
    coll_safe = collection.with_options(write_concern=WriteConcern(w="majority"))
    result = coll_safe.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

# 3. Strongly Consistent Read
@app.route(“/count-tesla-primary”, methods=[“GET”])
def count_tesla():
    coll_primary = collection.with_options(read_preference=ReadPreference.PRIMARY)
    count = coll_primary.count_documents({"Make": "TESLA"})
    return jsonify({"count": count})

# 4. Eventually Consistent Analytical Read
@app.route(“/count-bmw-secondary”, methods=[“GET”])
def count_bmw():
    coll_secondary = collection.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    count = coll_secondary.count_documents({"Make": "BMW"})
    return jsonify({"count": count})

if __name__ == “__main__”:
    app.run(host=”0.0.0.0”, port=5000)

