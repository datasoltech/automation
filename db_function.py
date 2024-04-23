import mysql.connector
import subprocess

# Define the authentication token
AUTH_TOKEN = 'apptoken'

# Path of the shell script to start MySQL

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
            'database': mysql_database,
            'user': mysql_user,
            'password': mysql_password
        }
        return {'success': True, 'output': result_json}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def connect_to_mysql(host, user, password, database=None):
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=host, 
            port='3306',   
            user=user,
            password=password,
            database='mydatabase'
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

def insert_database(result,status=True, sql_instance_type='mysql', backup_dir=None, replication_id=-1):
    try:
        conn = mysql.connector.connect(
            host='130.211.206.15',
            port='3306',
            user='rooot',
            password='BinRoot@123',
            database='mydatabase',
        )

        cursor = conn.cursor()

        # Create the 'monitor' database if it doesn't exist
        # cursor.execute("CREATE DATABASE IF NOT EXISTS monitor1")
        print("creating monitor1 database",result,flush=True)
        # Use the 'monitor' database
        cursor.execute("USE mydatabase")

        # Create table if not exists with status and sql_instance_type columns
        # Create the 'sql_instances' table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sql_instances (
            id INT AUTO_INCREMENT PRIMARY KEY,
            instance_name VARCHAR(255),
            external_ip VARCHAR(255),
            default_database VARCHAR(255),
            user VARCHAR(255),
            password VARCHAR(255),
            status BOOLEAN DEFAULT TRUE,
            sql_instance_type VARCHAR(255) DEFAULT 'mysql',
            backup_dir VARCHAR(255) DEFAULT NULL,
            replication_id INT DEFAULT -1
        )
        """
        cursor.execute(create_table_query)


         # Insert the instance data into the table
        insert_query = """
        INSERT INTO sql_instances (instance_name, external_ip, default_database, user, password, status, sql_instance_type, backup_dir, replication_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            result['output']['instance_name'],
            result['output']['external_ip'],
            result['output']['database'],
            result['output']['user'],
            result['output']['password'],status, sql_instance_type, backup_dir, replication_id
        ))

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()

        return {'success': True, 'message': 'Result stored in the database'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_all_instances(host, user, password):
    try:
        # Connect to MySQL database
        conn = connect_to_mysql(host, user, password)

        # Create cursor
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
                'default_database': row[3],
                'user': row[4],
                'password': row[5],
                'status': row[6],
                'sql_instance_type': row[7],
                'backup_dir': row[8],
                'replication_id': row[9]
            }
            mysql_instances.append(instance)

        # Close cursor and connection
        cursor.close()
        conn.close()

        return mysql_instances
    except Exception as e:
        raise Exception(f'MySQL error: {e}')
