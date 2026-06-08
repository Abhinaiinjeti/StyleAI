import sqlite3
import csv

conn = sqlite3.connect("outfit_recommender.db")
cursor = conn.cursor()

with open("outfits.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        cursor.execute("""
        INSERT INTO outfits (
            id,
            occasion,
            style,
            weather_type,
            skin_tone,
            body_type,
            top_wear,
            bottom_wear,
            footwear,
            accessories,
            image_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

conn.commit()
conn.close()

print(" records imported successfully!")