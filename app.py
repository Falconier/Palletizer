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

@app.route('/inventory_table', methods=['GET'])
def inventory_table():
    return render_template('inventory_table.html')

@app.route('/add_inventory', methods=['GET'])
def add_inventory_form():
    return render_template('add_inventory.html')

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()
    item_upc = data.get('item_upc')
    item_upc = str(item_upc).replace(" ","")
    if item_upc.isdigit() and (len(item_upc) == 12 or len(item_upc) == 13):
        item_upc = item_upc
    elif item_upc.isdigit() and len(item_upc) < 12:
        item_upc = item_upc.zfill(12)
    else:
        return jsonify({"error": "Invalid UPC code"}), 400
    
    item_upc = int(item_upc)
    if not item_upc:
        return jsonify({"error": "UPC code cannot be empty"}), 400

    item_mn = data.get('item_mn')
    item_pn = data.get('item_pn')
    item_name = data.get('item_name')
    item_desc = data.get('item_description')
    item_price = data.get('item_price') 
    items_per_pallet = int(data.get('items_per_pallet'))
    
    in_box = data.get('in_box')
    if in_box:
        items_per_box = int(data.get('items_per_box'))
    else:
        items_per_box = None
    
    seller_id = int(data.get('seller_id'))
    seller_sku = data.get('seller_sku')
    if seller_id == -1 and seller_sku != "":
        return jsonify({"error": "Seller must be selected if seller SKU is provided"}), 400
    if seller_id != -1 and seller_sku == "":
        return jsonify({"error": "Seller SKU must be provided if seller is selected"}), 400
    if seller_id == -1 and seller_sku == "":
        seller_id = None
        seller_sku = None

    print(type(item_upc), type(item_mn), type(item_pn), type(item_name), type(item_desc), type(item_price), type(items_per_pallet), type(in_box), type(items_per_box), type(seller_id), type(seller_sku))

    conn = get_db_connection()
    cursor = conn.cursor()
    ##cursor.execute('INSERT INTO inventory (item_upc, item_model_number, item_part_number, item_name, item_description, item_price, items_per_pallet, in_box, items_per_box) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
    ##           (item_upc, item_mn, item_pn, item_name, item_desc, item_price, items_per_pallet, in_box, items_per_box if in_box else None))
    cursor.execute('EXEC dbo.insert_inventory @item_upc=?, @item_model_number=?, @item_part_number=?, @item_name=?, @item_description=?, @item_price=?, @items_per_pallet=?, @in_box=?, @items_per_box=?, @inventory_seller_id=?, @seller_sku=?',
                   (item_upc, item_mn, item_pn, item_name, item_desc, item_price, items_per_pallet, 1 if in_box else 0, items_per_box if in_box else None, seller_id, seller_sku))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Item added successfully"}), 201

@app.route('/add_seller', methods=['GET'])
def add_seller_form():
    return render_template('add_seller.html')

@app.route('/add_seller', methods=['POST'])
def add_seller():
    data = request.get_json()
    seller_name = data.get('seller_name')
    seller_website = data.get('seller_website')

    if (not seller_name and not seller_website) or (seller_name == "" and seller_website == ""):
        return jsonify({"error": "Seller name and website cannot be empty"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO InventorySellers (seller_name, seller_url) VALUES (?, ?)', (seller_name, seller_website))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Seller added successfully"}), 201

@app.route('/sellers', methods=['GET'])
def get_sellers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT inventory_seller_id, seller_name FROM InventorySellers')
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    sellers_data = []
    for row in rows:
        sellers_data.append(dict(zip(columns, row)))
    return jsonify(sellers_data)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)