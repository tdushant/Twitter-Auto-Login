import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    try:
        db_connection = mysql.connector.connect(
            host=os.getenv('host'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            database=os.getenv('database')
        )
        if db_connection.is_connected():
            return db_connection
        else:
            return None
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def execute_query(query, values=None):
    db_connection = None
    cursor = None
    try:
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        db_connection.commit()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

def get_users():
    try:
        query = "SELECT DISTINCT ident FROM profiles WHERE type = 'twitter' AND name = '' AND ident IS NOT NULL"
        results = execute_query(query)
        
        users = [result[0] for result in results if result and result[0]]  # Unpack single-element tuples and filter out empty records
        
        if users:
            return users
        else:
            return None
    except Exception as e:
        print(f"Error fetching users: {e}")
        return None


def update_profile_name(ident, new_name):
    try:
        query = "UPDATE profiles SET name = %s WHERE ident = %s"
        values = (new_name, ident)
        execute_query(query, values)
    except Exception as e:
        print(f"Error updating profile name: {e}")

        
def update_profile_name_by_id(id, new_name):
    try:
        query = "UPDATE profiles SET name = %s WHERE id = %s"
        values = (new_name, id)
        execute_query(query, values)
    except Exception as e:
        print(f"Error updating profile name: {e}")
