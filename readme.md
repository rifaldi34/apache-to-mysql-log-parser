
# Apache Access Log Parser to MySQL

import apache access.log files into a mysql table

This Python script parses Apache access logs and inserts the log entries into a specified MySQL database table. It handles batch inserts for efficiency and supports datetime conversion to the MySQL `DATETIME` format.

## Requirements

- Python 3.x
- `mysql-connector-python` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/rifaldi34/apache-to-mysql-log-parser.git
    cd apache-log-parser
    ```

2. Install the required Python library:
    ```sh
    pip install mysql-connector-python
    ```

## Usage

```sh
python insert_logs.py <access_log_file> <mysql_host> <mysql_user> <mysql_password> <db_name> <table_name>
```

### Arguments

- `<access_log_file>`: Path to the Apache access log file.
- `<mysql_host>`: MySQL host (e.g., `localhost`).
- `<mysql_user>`: MySQL username.
- `<mysql_password>`: MySQL password.
- `<db_name>`: Name of the MySQL database.
- `<table_name>`: Name of the table to insert the log entries.

## Script Details

### Functions

- `parse_log_line(line)`: Parses a single line of the Apache access log.
- `convert_to_mysql_datetime(apache_datetime)`: Converts Apache log datetime to MySQL `DATETIME` format.
- `insert_logs(cursor, logs, table_name)`: Inserts logs into the specified table in batches.
- `create_table(cursor, table_name)`: Creates the specified table if it does not already exist.

### Flow

1. **Database Connection**: Establishes a connection to the specified MySQL database.
2. **Table Creation**: Creates the specified table if it does not exist.
3. **Log Parsing**: Reads the access log file line by line, parses each line, and converts the datetime format.
4. **Batch Insert**: Inserts log entries into the table in batches for efficiency.
5. **Commit and Close**: Commits the transaction and closes the database connection.

## Error Handling

The script includes basic error handling to catch and display database connection errors, table creation errors, and insertion errors.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
