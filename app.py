from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/insert", methods=["POST"])
def insert_data():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute("INSERT INTO data (name) VALUES (?) ", (data['name'], ))
    conn.commit()
    conn.close()
    return jsonify({"status": "Data inserted"})

@app.route("/data", methods=["GET"])
def get_data():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM data").fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_data():
    conn = get_db_connection()
    conn.execute("DELETE FROM data WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "Data deleted"})

if __name__ == "__main__":
    app.run(debug=True)
    