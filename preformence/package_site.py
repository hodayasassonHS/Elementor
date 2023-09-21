import json
import psycopg2
def insert_sites_to_package_data(data):
    
    db_params = {
        "host": 'test-rds-dev.colcjtm9obot.eu-west-1.rds.amazonaws.com',
        "database": "metrics_dev",
        "user": "developer",
        "password": "41b387c1-2cf9-4436-85fa-7c75093b7d14",
        "port":"5432"
    }




    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Iterate through the JSON data and insert into the table
        for entry in data:
          
                query = """
                INSERT INTO sites_to_package (site_id,package_id)
                VALUES (%s, %s);
                """
                values = (
                    entry["site_id"],
                    entry["user_package_id"]
                )
                cursor.execute(query, values)

        # Commit the changes and close the connection
        conn.commit()
        print("Data inserted successfully.")

    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        if conn is not None:
            conn.close()