from flask import Flask, render_template, request
import sqlite3
import os

from services.skin_tone import detect_skin_tone
from services.weather_service import get_weather

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = sqlite3.connect(
    "outfit_recommender.db",
    check_same_thread=False

)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        occasion = request.form['occasion']
        style = request.form['style']
        city = request.form['city']

        image = request.files.get('image')
        image_filename = ""
        skin_tone = "Medium"

        if image and image.filename:
            image_filename = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

            try:
                skin_tone = detect_skin_tone(image_path)
            except Exception:
                skin_tone = "Medium"

        weather_type = "Normal"
        temperature = 25

        try:
            weather_type, temperature = get_weather(city)
        except Exception:
            pass

        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        query = """
        SELECT *
        FROM outfits
        WHERE occasion=?
        AND style=?
        AND weather_type=?
        AND skin_tone=?
        ORDER BY image_url
        """

        cursor.execute(query, (occasion, style, weather_type, skin_tone))
        outfits = cursor.fetchall()

        if not outfits:
            fallback_query = """
            SELECT *
            FROM outfits
            WHERE occasion=?
            AND style=?
            AND weather_type=?
            ORDER BY image_url
            """

            cursor.execute(fallback_query, (occasion, style, weather_type))
            outfits = [dict(row) for row in cursor.fetchall()]

        return render_template(
            'result.html',
            outfits=outfits,
            image_filename=image_filename,
            skin_tone=skin_tone,
            weather_type=weather_type,
            temperature=temperature,
            city=city,
            occasion=occasion,
            style=style
        )

    return render_template('recommend.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)