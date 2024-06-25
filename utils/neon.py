"""
THIS SCRIPT IS USED TO INTERACT: READ/WRITE TO THE NEON_DB.
IN STREAMLIT SECRETS OR OS.ENVIRON SETUP THE LINK TO THE DB.
"""

import psycopg2
import os


def write_to_db(connection_string, table, data):
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        columns = ', '.join(data.keys())
        values = [data[col] for col in data.keys()]
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cur.execute(query, values)
        conn.commit()
        if cur:
            cur.close()
        if conn:
            conn.close()
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return e


def read_db(connection_string, table, condition='1=1', printout=False):
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE {condition}")
        rows = cur.fetchall()
        if printout:
            for row in rows:
                print(row)
        if cur:
            cur.close()
        if conn:
            conn.close()
        return rows
    except Exception as e:
        print(f"An error occurred: {e}")
        return e


def main():
    connection_string = os.environ["NEON_URL"]
    table_name = "home"
    print(f"len: {len(read_db(connection_string, table_name, printout=True))}")
    data_to_insert = {
        'id': 3,
        'name': "Elia",
        'pet': 'gator'
    }
    write_to_db(connection_string, table_name, data_to_insert)
    read_db(connection_string, table_name, printout=True)
    print(f"len: {len(read_db(connection_string, table_name, printout=True))}")


if __name__ == "__main__":
    main()
