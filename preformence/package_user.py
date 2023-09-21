import json
import psycopg2
def insert_packages_data(data):
    # PostgreSQL connection parameters
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
            user_id = entry["user_id"]
            package_id = entry["package_id"]

            # Check if the user_id and package_id exist in the respective tables
            user_check_query = "SELECT user_id FROM users WHERE user_id = %s;"
            package_check_query = "SELECT package_id FROM packages WHERE package_id = %s;"
            cursor.execute(user_check_query, (user_id,))
            user_exists = cursor.fetchone()
            cursor.execute(package_check_query, (package_id,))
            package_exists = cursor.fetchone()

            if user_exists and package_exists:
                query = """
                INSERT INTO packages_to_users (package_to_user_id, user_id, package_id)
                VALUES (%s, %s, %s);
                """
                values = (
                    entry["package_user_id"],
                    entry["user_id"],
                    entry["package_id"]
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
