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

@app.route('/inventory', methods=['GET'])
def inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()

    inventory_data = []
    for row in rows:
        inventory_data.append(dict(zip(columns, row)))

    return jsonify(inventory_data)

@app.route('/inventory_table')
def inventory_table():
    return render_template('inventory_table.html')

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()
    item_upc = data.get('item_upc')
    item_mn = data.get('item_model_number')
    item_pn = data.get('item_part_number')
    item_name = data.get('item_name')
    item_desc = data.get('item_description')
    item_price = data.get('item_price') 
    items_per_pallet = data.get('items_per_pallet')
    in_box = data.get('in_box')
    if in_box:
        items_per_box = data.get('items_per_box')
    
    item_upc = str(item_upc).replace(" ","")
    if item_upc.isdigit() and len(item_upc) == 12:
        item_upc = item_upc
    elif item_upc.isdigit() and len(item_upc) < 12:
        item_upc = item_upc.zfill(12)
    else:
        return jsonify({"error": "Invalid UPC code"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO inventory (item_upc, item_model_number, item_part_number, item_name, item_description, item_price, items_per_pallet, in_box, items_per_box) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
               (item_upc, item_mn, item_pn, item_name, item_desc, item_price, items_per_pallet, in_box, items_per_box if in_box else None))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Item added successfully"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)