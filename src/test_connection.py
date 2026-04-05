
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pune@123",
    database="finance_db"
)

print("Connected to MySQL successfully!")
