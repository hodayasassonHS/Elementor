import psycopg2
import json

# Function to insert data into the database
def insert_users_data(data):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
        host='test-rds-dev.colcjtm9obot.eu-west-1.rds.amazonaws.com',
        dbname="metrics_dev",
        user="developer",
        password="41b387c1-2cf9-4436-85fa-7c75093b7d14",
        port="5432"
        )

        cursor = connection.cursor()

        # Loop through each user in the JSON data
        for user in data:
            # Convert user_id to UUID type
            user_id = user['user_id']

            # Convert the phone_number to text to match the table's datatype
            phone_number = str(user['phone_number'])

            # Construct the SQL query
            sql_query = """INSERT INTO users (user_id, first_name, last_name, email, address, phone_number,password)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)  ;"""

            # Execute the SQL query
            cursor.execute(sql_query, (
                user['user_id'], user['first_name'], user['last_name'],
                user['email'], user['address'], phone_number,user['password']
            ))

        # Commit the changes
        connection.commit()
        print("Data inserted successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or inserting data:", error)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    # Read the JSON file
    with open("fake_users.json", "r") as file:
        json_data = json.load(file)

    # Call the function to insert the data into the database
    insert_users_data(json_data)
