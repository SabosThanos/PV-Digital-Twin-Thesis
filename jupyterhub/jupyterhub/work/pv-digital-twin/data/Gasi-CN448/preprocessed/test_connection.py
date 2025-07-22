import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': "postgres",
    'password': 'bhSfWIhKfNGHoE0AZF6grXOqa1UcMAiJnQdQWnW6XqtmFnrsXOGBeCWcxM2kBwA4',
    'host': 'localhost',
    'port': '5432'
}

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    # Execute a simple query
    cur.execute("SELECT version();")
    print("PostgreSQL version:", cur.fetchone())

    # Close the connection
    cur.close()
    conn.close()
    
except Exception as e:
    print("Error:", e)