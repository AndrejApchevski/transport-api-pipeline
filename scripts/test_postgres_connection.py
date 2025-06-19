import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="transport_data",
    user="postgres",
    password="1000lordofrings"  # Replace with your real password
)

cur = conn.cursor()
cur.execute("SELECT version();")
print("PostgreSQL version:", cur.fetchone())

cur.close()
conn.close()
