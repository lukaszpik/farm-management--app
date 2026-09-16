import psycopg
from psycopg.rows import dict_row


connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="farm-management",
    user="postgres",
    password="admin",
    row_factory=dict_row
)

print("Connected with database successfully.")
