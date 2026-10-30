import csv
import getpass
from pathlib import Path
import mysql.connector

csv_path = Path.home() / "Downloads/olist-ecommerce-analysis/data/olist_order_reviews_utf8.csv"

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
CREATE TABLE IF NOT EXISTS order_reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date VARCHAR(30),
    review_answer_timestamp VARCHAR(30)
)
""")

cursor.execute("SELECT COUNT(*) FROM order_reviews")
existing_rows = cursor.fetchone()[0]

if existing_rows > 0:
    print(f"Stopped safely: order_reviews already has {existing_rows} rows.")
else:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        batch = []

        for row in reader:
            batch.append((
                row["review_id"] or None,
                row["order_id"] or None,
                int(row["review_score"]) if row["review_score"] else None,
                row["review_comment_title"] or None,
                row["review_comment_message"] or None,
                row["review_creation_date"] or None,
                row["review_answer_timestamp"] or None,
            ))

            if len(batch) >= 1000:
                cursor.executemany("""
                    INSERT INTO order_reviews
                    (review_id, order_id, review_score, review_comment_title,
                     review_comment_message, review_creation_date, review_answer_timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, batch)
                connection.commit()
                batch.clear()

        if batch:
            cursor.executemany("""
                INSERT INTO order_reviews
                (review_id, order_id, review_score, review_comment_title,
                 review_comment_message, review_creation_date, review_answer_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, batch)
            connection.commit()

    cursor.execute("SELECT COUNT(*) FROM order_reviews")
    print("Import finished. Rows in order_reviews:", cursor.fetchone()[0])

cursor.close()
connection.close()
