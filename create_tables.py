import psycopg2
host = "test-rds-dev.colcjtm9obot.eu-west-1.rds.amazonaws.com"
port = 5432
database = "metrics_dev"
user = "developer"
password = "41b387c1-2cf9-4436-85fa-7c75093b7d14"
# Connect to the default database (e.g., "postgres")
connection = psycopg2.connect(
    host=host,
    port=port,
    database="postgres",
    user="user",
    password=password
)
connection.autocommit = True
cursor = connection.cursor()
print("Connected to the default database!")
# Close the cursor and connection to the default database
cursor.close()
connection.close()
print("Disconnected from the default database!")
# Connect to the metrics_dev database
connection = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)
cursor = connection.cursor()
print(f"Connected to the {database} database!")
# Execute the SQL statements to create the tables
sql_statements = '''
    -- Table: users
    -- Stores information about users
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        address TEXT,
        phone_number TEXT,
    );
    -- Table: packages
    -- Stores information about packages
    CREATE TABLE packages (
        package_id SERIAL PRIMARY KEY,
        cost_per_month INT,
        storage_gb FLOAT,
        disc_cache FLOAT,
        disc_a_gb FLOAT,
        disc_b_gb FLOAT,
        cpu_percent FLOAT,
        cpu_tic FLOAT,
    );
    -- Table: packages_to_users
    -- Represents the relationship between users and packages
    CREATE TABLE packages_to_users (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id),
        package_id INT REFERENCES packages(package_id)
    );
    -- Table: usage_per_site
    -- Stores usage information per site
    CREATE TABLE usage_per_site (
        id SERIAL PRIMARY KEY,
        packages_to_user_id INT REFERENCES packages_to_users(id),
        time TIMESTAMPTZ,
        storage_gb FLOAT,
        disc_cache FLOAT,
        disc_a_gb FLOAT,
        disc_b_gb FLOAT,
        cpu_percent FLOAT,
        cpu_tic FLOAT,
    );
    -- Table: sites
    -- Stores information about sites
    CREATE TABLE sites (
        site_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id)
    );
    -- Table: metrics
    -- Stores information about metrics
    CREATE TABLE metrics(
        event_uuid SERIAL PRIMARY KEY,
        event_time TIMESTAMPTZ,
        site_id INT REFERENCES sites(site_id),
        storage_gb FLOAT,
        disc_cache FLOAT,
        disc_a_gb FLOAT,
        disc_b_gb FLOAT,
        cpu_percent FLOAT,
        cpu_tic FLOAT,
    );
'''
cursor.execute(sql_statements)
connection.commit()
print("Tables created successfully!")
# Close the cursor and connection to the metrics_dev database
cursor.close()
connection.close()
print(f"Disconnected from the {database} database!")