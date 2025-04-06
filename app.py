import os
import mysql.connector
import pandas as pd
import json
import pytz
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask_cors import CORS  # <--- IMPORTANTE!

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'sunflower_trade')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # <--- ATIVA CORS para todos os domínios

# Configurar pasta de imagens estáticas
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

# Connect to MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None

# Get list of all items in the database
def get_all_items():
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT item_name FROM item_prices ORDER BY item_name")
        items = [row[0] for row in cursor.fetchall()]
        return items
    except mysql.connector.Error as err:
        print(f"Error fetching items: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Get price data for a specific item
def get_item_price_history(item_name, days=30):
    connection = connect_to_db()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        query = """
        SELECT 
            item_name, 
            p2p_price, 
            seq_price, 
            ge_price, 
            timestamp 
        FROM 
            item_prices 
        WHERE 
            item_name = %s AND 
            timestamp BETWEEN %s AND %s 
        ORDER BY 
            timestamp
        """
        
        cursor.execute(query, (item_name, start_date, end_date))
        results = cursor.fetchall()
        
        if results:
            df = pd.DataFrame(results)
            df['timestamp'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
            return df.to_dict('records')
        else:
            return []
    except mysql.connector.Error as err:
        print(f"Error fetching price history: {err}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Routes
@app.route('/')
def index():
    items = get_all_items()
    # Serve index.html from root directory instead of templates folder
    return send_from_directory('.', 'index.html')

@app.route('/api/items')
def api_items():
    items = get_all_items()
    return jsonify(items)

@app.route('/api/price_history')
def api_price_history():
    item_name = request.args.get('item', '')
    days = int(request.args.get('days', 30))
    
    if not item_name:
        return jsonify({'error': 'Item name is required'}), 400
    
    data = get_item_price_history(item_name, days)
    if data is None:
        return jsonify({'error': 'Failed to fetch price history'}), 500
    
    for item in data:
        if 'timestamp' in item:
            dt = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')
            item['timestamp'] = dt.strftime('%d/%m/%Y %H:%M:%S')
        
        if item['p2p_price'] is not None:
            item['p2p_price'] = float(format(item['p2p_price'], '.4f'))
            item['p2p_discount'] = float(format(item['p2p_price'] * 0.9, '.4f'))
        else:
            item['p2p_discount'] = None
        
        if item['seq_price'] is not None:
            item['seq_price'] = float(format(item['seq_price'], '.4f'))
        if item['ge_price'] is not None:
            item['ge_price'] = float(format(item['ge_price'], '.4f'))
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
