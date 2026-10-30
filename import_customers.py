import csv
import getpass
from pathlib import Path
import mysql.connector

csv_path = Path.home() / "Downloads/olist-ecommerce-analysis/data/olist_customers_utf8.csv"

if not csv_path.exists():
    raise FileNotFoundError(f"CSV not found: {csv_path}")

password = getpass.getpass("Enter the olist_importer password: ")

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="olist_importer",
    password=password,
    database="olist_portfolio",
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(100),
    customer_state VARCHAR(5)
)
""")

cursor.execute("SELECT COUNT(*) FROM customers")
existing_rows = cursor.fetchone()[0]

if existing_rows > 0:
    print(f"Stopped safely: customers already has {existing_rows} rows.")
else:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        batch = []

        for row in reader:
            batch.append((
                row["customer_id"] or None,
                row["customer_unique_id"] or None,
                row["customer_zip_code_prefix"] or None,
                row["customer_city"] or None,
                row["customer_state"] or None,
            ))

            if len(batch) >= 1000:
                cursor.executemany("""
                    INSERT INTO customers
                    (customer_id, customer_unique_id, customer_zip_code_prefix,
                     customer_city, customer_state)
                    VALUES (%s, %s, %s, %s, %s)
                """, batch)
                connection.commit()
                batch.clear()

        if batch:
            cursor.executemany("""
                INSERT INTO customers
                (customer_id, customer_unique_id, customer_zip_code_prefix,
                 customer_city, customer_state)
                VALUES (%s, %s, %s, %s, %s)
            """, batch)
            connection.commit()

    cursor.execute("SELECT COUNT(*) FROM customers")
    print("Import finished. Rows in customers:", cursor.fetchone()[0])

cursor.close()
connection.close()
