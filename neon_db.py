import os
import psycopg2

def write_to_db(cur, table, data):
    try:
        # Fetch column names from the table
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
        columns = [row[0] for row in cur.fetchall() if row[0] != 'id']  # Assuming 'id' is auto-increment

        # Prepare the SQL command using the column names
        columns_sql = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"INSERT INTO {table} ({columns_sql}) VALUES ({placeholders})"

        # Execute SQL command to write to the database
        cur.executemany(query, data)
    except Exception as e:
        print(f"An error occurred: {e}")

def read_db(cur, table, criteria='1=1'):
    try:
        # Execute a select statement to read the data
        cur.execute(f"SELECT * FROM {table} WHERE {criteria}")
        rows = cur.fetchall()

        for row in rows:
            print(row)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    connection_string = os.environ.get('NEON_URL')
    connection_string = "postgresql://circ_db_owner:****@ep-square-art-a2iq8s9s.eu-central-1.aws.neon.tech/circ_db?sslmode=require"
    connection_string = "postgresql://circ_db_owner:****@ep-tiny-star-a208v1dr.eu-central-1.aws.neon.tech/circ_db?sslmode=require"
    connection_string = "postgresql://circ_db_owner:****@ep-tiny-star-a208v1dr.eu-central-1.aws.neon.tech/circ_db?sslmode=require"

    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()

        #table_name = "users"
        table_name = "geb"
        #data_to_insert = [("1.1.10", "John", "123456", "myemail", "mycomp"), ("1.3.10", "Jane", "45678", "janeemail", "janecomp")]

        sample_tuple = (
            1200,
            1990,  # baujahr (integer)
            "johndoe",  # user_name (TEXT NOT NULL)
            "Residential",  # nutzung (TEXT)
            "Initial",  # datenstufe (TEXT)
            "webscraper"  # autor (TEXT)
            "neu",  # typ (TEXT)
            "Neubau EFH",  # name (TEXT NOT NULL)
            "1234 Main St.",  # adresse (TEXT)
            )

        data_to_insert = [sample_tuple]

        # Perform database operations
        read_db(cur, table_name)
        a = input("test")
        write_to_db(cur, table_name, data_to_insert)
        conn.commit()  # Commit changes

        print("\nReading specific entries from the database:")
        read_db(cur, table_name)

    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()

