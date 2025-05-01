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

@app.route('/')
def index():
    return render_template('/add_inventory.html')

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()
    item_upc = data.get('item_upc')
    item_mn = data.get('item_model_number')
    item_pn = data.get('item_part_number')
    item_name = data.get('item_name')
    item_desc = data.get('item_description')
    item_price = data.get('item_price')
    item_cost = data.get('item_cost')
    items_per_pallet = data.get('items_per_pallet')
    in_box = data.get('in_box')
    if in_box:
        items_per_box = data.get('items_per_box')
    
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('Insert into inventory (item_upc, item_model_number, item_part_number, item_name, item_description, item_price, item_cost, items_per_pallet, in_box, items_per_box) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (item_upc, item_mn, item_pn, item_name, item_desc, item_price, item_cost, items_per_pallet, in_box, items_per_box if in_box else None))               
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Item added successfully"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)