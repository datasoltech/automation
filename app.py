from flask import Flask, jsonify, request
from flask_cors import CORS
from db_function import *

app = Flask(__name__)
CORS(app)

# Define the authentication token
AUTH_TOKEN = 'apptoken'

# Path of the shell script to start services
START_MYSQL_SCRIPT_PATH = '/home/flask-api/mysql.sh'
START_PGSQL_SCRIPT_PATH = '/home/flask-api/postgres.sh'
START_CLOUDSQLM_SCRIPT_PATH = '/home/flask-api/cloudsql-MS.sh'
START_CLOUDSQLP_SCRIPT_PATH ='/home/flask-api/cloudsql-p.sh'
START_ALLOYDBOMINI_SCRIPT_PATH = '/home/flask-api/alloyomini.sh'


@app.route('/start_alloydbOMINI', methods=['POST'])
def start_alloydbOMINI():
    try:
        # Check if the authentication token is provided
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        print('here', flush=True)
        script_path = '/home/flask-api/alloyomini.sh'
        result = execute_shell_script(START_ALLOYDBOMINI_SCRIPT_PATH)
        insert_result=insert_database(
        result,sql_instance_type='pgsql')
        print('here   ', flush=True)
        if insert_result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/start_cloudsqlP', methods=['POST'])
def start_cloudsqlP():
    try:
        # Check if the authentication token is provided
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        print('here', flush=True)
        script_path = '/home/flask-api/cloudsql-p.sh '
        result = execute_shell_script(START_CLOUDSQLP_SCRIPT_PATH)
        insert_result=insert_database(
        result,sql_instance_type='pgsql')
        print('here   ', flush=True)
        if insert_result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/start_cloudsqlM', methods=['POST'])
def start_cloudsqlM():
    try:
        # Check if the authentication token is provided
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        print('here', flush=True)
        script_path = '/home/flask-api/cloudsql-MS.sh'
        result = execute_shell_script(START_CLOUDSQLM_SCRIPT_PATH)
        insert_result=insert_database(
        result,sql_instance_type='mysql')
        print('here   ', flush=True)
        if insert_result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/start_postgres', methods=['POST'])
def start_postgres():
    try:
        # Check if the authentication token is provided
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        print('here', flush=True)
        script_path = '/home/flask-api/postgres.sh'
        result = execute_shell_script(START_PGSQL_SCRIPT_PATH)
        insert_result=insert_database(
        result,sql_instance_type='pgsql')
        print('here   ', flush=True)
        if insert_result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/start_mysql', methods=['POST'])
def start_mysql():
    auth_token = request.headers.get('Authorization')
    if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
    print('here', flush=True)
 
    
    # Execute the MySQL start script and get the result
    result = execute_shell_script(START_MYSQL_SCRIPT_PATH)


    # Insert the result into the database
    try:
        # Check if the authentication token is provided
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 401
        print('here', flush=True)
            # Your existing code to start MySQL and obtain the result object
        result = execute_shell_script(START_MYSQL_SCRIPT_PATH)
        insert_database(
        result,sql_instance_type='mysql')

        return jsonify({'success': True, 'message': 'Result stored in the database'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/get_mysql_instances', methods=['GET'])
def get_mysql_instances():
    try:
        # Call the function to get all instances from the database
        instances = get_all_instances(
            host='130.211.206.15',
            user='rooot',
            password='BinRoot@123'
        )
        return jsonify({'mysql_instances': instances}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
