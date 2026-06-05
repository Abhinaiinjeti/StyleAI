import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="abhinai25",
    database="outfit_recommender"
)

cursor = db.cursor()

cursor.execute("SELECT * FROM outfits")

rows = cursor.fetchall()

for row in rows:
    print(row)