from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('growbox_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
