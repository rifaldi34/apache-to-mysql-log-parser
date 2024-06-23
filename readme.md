# Apache Access Log Parser to MySQL

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
