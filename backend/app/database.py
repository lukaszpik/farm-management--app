import psycopg


connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="farm-management",
    user="postgres",
    password="admin"
)

print("Connected with database successfully.")
connection.close()