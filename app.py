from flask import Flask, jsonify, request, render_template
import pyodbc
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

conn_str = (f"DRIVER={os.getenv('DB_DRIVER')};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')};")

def get_db_connection():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Connection failed: {e}")
        raise



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)