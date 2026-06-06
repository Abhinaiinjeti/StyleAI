import sqlite3

conn = sqlite3.connect("outfit_recommender.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS outfits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    occasion TEXT NOT NULL,
    style TEXT NOT NULL,
    weather_type TEXT NOT NULL,
    skin_tone TEXT NOT NULL,
    body_type TEXT NOT NULL,
    top_wear TEXT NOT NULL,
    bottom_wear TEXT NOT NULL,
    footwear TEXT NOT NULL,
    accessories TEXT,
    image_url TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")