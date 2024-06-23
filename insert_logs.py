import mysql.connector
from mysql.connector import Error
import re
import sys
from datetime import datetime

def parse_log_line(line):
    """
    Parse a single line of the Apache access log.
    Adjust the regex pattern according to your log format.
    """
    log_pattern = re.compile(
        r'(?P<ip>\S+) (?P<identd>\S+) (?P<user>\S+) \[(?P<datetime>[^\]]+)\] "(?P<request>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\S+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    )
    match = log_pattern.match(line)
    if match:
        log_data = match.groupdict()
        log_data['datetime'] = convert_to_mysql_datetime(log_data['datetime'])
        return log_data
    return None

def convert_to_mysql_datetime(apache_datetime):
    """
    Convert Apache log datetime to MySQL datetime format.
    Example input: 11/May/2024:23:22:48 +0700
    Example output: 2024-05-11 23:22:48
    """
    return datetime.strptime(apache_datetime.split()[0], "%d/%b/%Y:%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

def insert_logs(cursor, logs, table_name):
    """
    Insert logs into the database in batches.
    """
    query = f"""
    INSERT INTO {table_name} (ip, identd, user, datetime, request, status, size, referer, user_agent)
    VALUES (%(ip)s, %(identd)s, %(user)s, %(datetime)s, %(request)s, %(status)s, %(size)s, %(referer)s, %(user_agent)s)
    """
    cursor.executemany(query, logs)

def create_table(cursor, table_name):
    """
    Create the specified table if it does not already exist.
    """
    try:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip VARCHAR(45),
            identd VARCHAR(255),
            user VARCHAR(255),
            datetime DATETIME,
            request TEXT,
            status INT,
            size VARCHAR(255),
            referer TEXT,
            user_agent TEXT
        )
        """)
        print(f"Table '{table_name}' created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")

def main():
    if len(sys.argv) != 7:
        print("Usage: python insert_logs.py <access_log_file> <mysql_host> <mysql_user> <mysql_password> <db_name> <table_name>")
        sys.exit(1)

    log_file = sys.argv[1]
    mysql_host = sys.argv[2]
    mysql_user = sys.argv[3]
    mysql_password = sys.argv[4]
    db_name = sys.argv[5]
    table_name = sys.argv[6]

    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=db_name
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Create table
            create_table(cursor, table_name)

            logs = []
            batch_size = 1000

            with open(log_file, 'r') as file:
                for line in file:
                    log = parse_log_line(line)
                    if log:
                        logs.append(log)
                    if len(logs) >= batch_size:
                        insert_logs(cursor, logs, table_name)
                        connection.commit()
                        logs = []

            # Insert any remaining logs
            if logs:
                insert_logs(cursor, logs, table_name)
                connection.commit()

            print("Logs inserted successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()
