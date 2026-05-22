import sqlite3

# CONNECT DATABASE
conn = sqlite3.connect("fraud_detection.db")

# CREATE CURSOR
cursor = conn.cursor()

# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    transaction_type TEXT,
    device_risk INTEGER,
    prediction TEXT,
    fraud_score REAL
)
""")

conn.commit()
conn.close()

print("✅ Database Created Successfully")