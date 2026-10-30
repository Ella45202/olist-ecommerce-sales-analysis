
import csv
import getpass
from pathlib import Path
import mysql.connector

BASE_DIR = Path.home() / "Downloads" / "olist-ecommerce-analysis"
CSV_FILE = BASE_DIR / "data" / "category_translation_utf8.csv"

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="olist_importer",
    password=getpass.getpass("MySQL password: "),
    database="olist_portfolio"
)

try:
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_translation (
            product_category_name VARCHAR(100),
            product_category_name_english VARCHAR(100)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM category_translation")
    existing_rows = cursor.fetchone()[0]

    if existing_rows > 0:
        print(f"Table already contains {existing_rows} rows. No data inserted.")
    else:
        with CSV_FILE.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            reader = csv.DictReader(file)
            rows = [
                (
                    row["product_category_name"],
                    row["product_category_name_english"]
                )
                for row in reader
            ]

        cursor.executemany("""
            INSERT INTO category_translation (
                product_category_name,
                product_category_name_english
            ) VALUES (%s, %s)
        """, rows)

        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM category_translation")
        print("Import finished. Rows in category_translation:",
              cursor.fetchone()[0])

finally:
    cursor.close()
    connection.close()

