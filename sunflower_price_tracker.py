import requests
import mysql.connector
import time
import datetime
import json
import os
import pytz
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', 3306))  # Pega a porta com fallback
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# API URL
API_URL = 'https://sfl.world/api/v1/prices'

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

# Create database and table if they don't exist
def setup_database():
    try:
        # Connect to MySQL server without specifying a database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # Create table for storing prices
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS item_prices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(50) NOT NULL,
            p2p_price DECIMAL(20, 8),
            seq_price DECIMAL(20, 8),
            ge_price DECIMAL(20, 8),
            timestamp DATETIME NOT NULL,
            updated_text VARCHAR(50),
            INDEX (item_name, timestamp)
        )
        """)
        
        connection.commit()
        print("Database and table setup completed successfully.")
        return True
    except mysql.connector.Error as err:
        print(f"Error setting up database: {err}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# Fetch data from API
def fetch_price_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return None

# Insert data into database
def insert_price_data(data):
    if not data:
        return
    
    connection = connect_to_db()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        # Use local system time directly
        timestamp = datetime.datetime.now()
        updated_text = data.get('updated_text', '')
        
        # Process p2p prices
        for item_name, price in data['data']['p2p'].items():
            seq_price = data['data']['seq'].get(item_name, None)
            ge_price = data['data']['ge'].get(item_name, None)
            
            cursor.execute("""
            INSERT INTO item_prices (item_name, p2p_price, seq_price, ge_price, timestamp, updated_text)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (item_name, price, seq_price, ge_price, timestamp, updated_text))
        
        # Check for items that are in seq or ge but not in p2p
        for market, prices in data['data'].items():
            if market == 'p2p':
                continue
                
            for item_name, price in prices.items():
                if item_name not in data['data']['p2p']:
                    p2p_price = None
                    seq_price = data['data']['seq'].get(item_name, None) if market != 'seq' else price
                    ge_price = data['data']['ge'].get(item_name, None) if market != 'ge' else price
                    
                    cursor.execute("""
                    INSERT INTO item_prices (item_name, p2p_price, seq_price, ge_price, timestamp, updated_text)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (item_name, p2p_price, seq_price, ge_price, timestamp, updated_text))
        
        connection.commit()
        print(f"Data inserted successfully at {timestamp}")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main function to run the script
def main():
    print("Starting Sunflower Land price tracker...")
    
    # Setup database and table
    if not setup_database():
        print("Failed to setup database. Exiting.")
        return
    
    print(f"Script will fetch prices every 5 minutes from {API_URL}")
    
    try:
        while True:
            print("\nFetching price data...")
            data = fetch_price_data()
            if data:
                insert_price_data(data)
            else:
                print("Failed to fetch or process data.")
            
            # Wait for 5 minutes before the next fetch
            print("Waiting for 5 minutes before next update...")
            time.sleep(900)  # 900 seconds = 15 minutes
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()