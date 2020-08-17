import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_cashier"
)
cursor = db.cursor()
# cursor.execute("CREATE DATABASE db_cashier")
