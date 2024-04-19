from flask import Flask, jsonify, request
import subprocess
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the authentication token
AUTH_TOKEN = 'apptoken'

# Path of the shell script to start MySQL
START_MYSQL_SCRIPT_PATH = '/home/flask_app/mysql.sh'

# Execute a shell script
def execute_shell_script(script_path):
    try:
        result = subprocess.run(['bash', script_path], capture_output=True, text=True)
        output = result.stdout
        # Extract relevant information
        lines = output.split('\n')
        instance_name = lines[0].split(': ')[1]
        external_ip = lines[1].split(': ')[1]
        mysql_database = lines[2].split(': ')[1]
        mysql_user = lines[3].split(': ')[1]
        mysql_password = lines[4].split(': ')[1]
        # Create JSON object
        result_json = {
            'instance_name': instance_name,
            'external_ip': external_ip,
            'mysql_database': mysql_database,
            'mysql_user': mysql_user,
            'mysql_password': mysql_password
        }
        return {'success': True, 'output': result_json}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def connect_to_mysql(host, user, password, database=None):
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as err:
        raise Exception(f'MySQL error: {err}')

def get_databases_and_tables(host, user, password):
    try:
        # Connect to MySQL without specifying a database
        conn = connect_to_mysql(host, user, password)

        # Create cursor
        cursor = conn.cursor()

        # Get list of databases
        cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in cursor.fetchall() if database[0] != 'performance_schema']

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Create a list to store database names and their respective table names
        db_tables_list = []

        # Iterate through databases and get their tables
        for db in databases:
            conn = connect_to_mysql(host, user, password, db)
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            conn.close()
            db_tables_list.append({'database': db, 'tables': tables})

        return db_tables_list
    except mysql.connector.Error as err:
        raise Exception(f'MySQL error: {err}')



@app.route('/start_mysql', methods=['POST'])
def start_mysql():
    # Check if the authorization token is provided
    if 'Authorization' not in request.headers or request.headers['Authorization'] != f'Bearer {AUTH_TOKEN}':
        return jsonify({'error': 'Unauthorized access'}), 401
    
    # Execute the MySQL start script and get the result
    result = execute_shell_script(START_MYSQL_SCRIPT_PATH)

    # Connect to MySQL database to store the result
    try:
        conn = mysql.connector.connect(
            host='35.244.61.106',
            port='3306',
            user='rooot',
            password='BinRoot@123',
            database='my_database' ,
        )

        cursor = conn.cursor()

        # Create the 'monitor' database if it doesn't exist
        #cursor.execute("CREATE DATABASE IF NOT EXISTS monitor1")
        print("creating monitor1 database")
        # Use the 'monitor' database
        cursor.execute("USE my_database")

        # Create table if not exists with status and sql_instance_type columns
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sql_instances (
            id INT AUTO_INCREMENT PRIMARY KEY,
            instance_name VARCHAR(255),
            external_ip VARCHAR(255),
            mysql_database VARCHAR(255),
            mysql_user VARCHAR(255),
            mysql_password VARCHAR(255),
            status BOOLEAN DEFAULT TRUE,
            sql_instance_type VARCHAR(255) DEFAULT 'mysql'
        )
        """
        cursor.execute(create_table_query)

        # Insert the result into the table with default values for status and sql_instance_type
        insert_query = """
        INSERT INTO sql_instances (instance_name, external_ip, mysql_database, mysql_user, mysql_password)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            result['output']['instance_name'],
            result['output']['external_ip'],
            result['output']['mysql_database'],
            result['output']['mysql_user'],
            result['output']['mysql_password']
        ))

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Result stored in the database'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/db_tables', methods=['POST'])
def get_db_tables():
    try:
        data = request.get_json()
        host = data.get('host')
        user = data.get('user')
        password = data.get('password')

        if not host or not user or not password:
            return jsonify({'error': 'Missing host, user, or password in request body'}), 400

        db_tables = get_databases_and_tables(host, user, password)
        return jsonify({'databases_tables': db_tables}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_mysql_instances', methods=['GET'])
def get_mysql_instances():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
         host='35.244.61.106',
            port='3306',
            user='rooot',
            password='BinRoot@123',
            database='my_database'
                )

        cursor = conn.cursor()

        # Execute query to retrieve all rows from sql_instances table
        cursor.execute("SELECT * FROM sql_instances")

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries for JSON response
        mysql_instances = []
        for row in rows:
            instance = {
                'instance_name': row[1],
                'external_ip': row[2],
                'mysql_database': row[3],
                'mysql_user': row[4],
                'mysql_password': row[5]
            }
            mysql_instances.append(instance)

        # Close cursor and connection
        cursor.close()
        conn.close()

        return jsonify({'mysql_instances': mysql_instances}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on loopback IP and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
