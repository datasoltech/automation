from flask import Flask, jsonify, request
from flask_cors import CORS
from db_function import *
import subprocess

app = Flask(__name__)
CORS(app)

# Define the authentication token
AUTH_TOKEN = 'apptoken'

# Path of the shell scripts
START_MYSQL_SCRIPT_PATH = '/home/flask-api/mysql.sh'
START_PGSQL_SCRIPT_PATH = '/home/flask-api/postgres.sh'
START_CLOUDSQLM_SCRIPT_PATH = '/home/flask-api/cloudsql-MS.sh'
START_CLOUDSQLP_SCRIPT_PATH = '/home/flask-api/cloudsql-p.sh'
START_ALLOYDBOMINI_SCRIPT_PATH = '/home/flask-api/alloyomini.sh'
DELETE_VM_SCRIPT_PATH = '/home/flask-api/delete.sh'


MYSQL_CONFIG = {
    'host': '34.42.230.148',
    'user': 'rooot',
    'password': 'BinRoot@123',
    'database': 'mydatabase'
}

@app.route('/start_alloydbOMINI', methods=['POST'])
def start_alloydbOMINI():
    try:
        # Check if the authentication token is provided
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        
        result = execute_shell_script(START_ALLOYDBOMINI_SCRIPT_PATH)
        insert_result = insert_database(result, sql_instance_type='pgsql')

        if insert_result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/start_cloudsqlP', methods=['POST'])
def start_cloudsqlP():
    try:
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        
        result = execute_shell_script(START_CLOUDSQLP_SCRIPT_PATH)
        insert_result = insert_database(result, sql_instance_type='pgsql')

        if insert_result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/start_cloudsqlM', methods=['POST'])
def start_cloudsqlM():
    try:
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        
        result = execute_shell_script(START_CLOUDSQLM_SCRIPT_PATH)
        insert_result = insert_database(result, sql_instance_type='mysql')

        if insert_result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/start_postgres', methods=['POST'])
def start_postgres():
    try:
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        
        result = execute_shell_script(START_PGSQL_SCRIPT_PATH)
        insert_result = insert_database(result, sql_instance_type='pgsql')

        if insert_result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/start_mysql', methods=['POST'])
def start_mysql():
    try:
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        
        result = execute_shell_script(START_MYSQL_SCRIPT_PATH)
        insert_result = insert_database(result, sql_instance_type='mysql')

        if insert_result['success']:
            return jsonify({'success': True, 'message': 'Result stored in the database'}), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_mysql_instances', methods=['GET'])
def get_mysql_instances():
    try:
        instances = get_all_instances(
            host='34.42.230.148',
            user='rooot',
            password='BinRoot@123'
        )
        return jsonify({'mysql_instances': instances}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete_vm', methods=['POST'])
def delete_vm():
    try:
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401

        instance_name = request.json.get('instance_name')
        subprocess.run(['bash', DELETE_VM_SCRIPT_PATH, instance_name], check=True)

        # Establish connection to MySQL database
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()

        # Execute UPDATE query to set status to 0
        update_query = "UPDATE sql_instances SET status = 0 WHERE instance_name = %s"
        cursor.execute(update_query, (instance_name,))
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()

        response = {"message": f"VM instance {instance_name} successfully deleted."}
        status_code = 200
    except subprocess.CalledProcessError:
        response = {"message": f"Failed to delete VM instance {instance_name}."}
        status_code = 500
    except Exception as e:
        response = {"message": str(e)}
        status_code = 500

    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
