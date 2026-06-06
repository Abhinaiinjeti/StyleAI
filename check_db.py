import sqlite3

conn = sqlite3.connect("outfit_recommender.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM outfits")

print(cursor.fetchone())

conn.close()