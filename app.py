from flask import Flask, render_template, request
import mysql.connector
import os

from services.skin_tone import detect_skin_tone
from services.weather_service import get_weather

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="abhinai25",
    database="outfit_recommender"
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
        skin_tone = "Unknown"

        if image and getattr(image, 'filename', ''):
            image_filename = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)
            skin_tone = detect_skin_tone(image_path)

        weather_type = "Normal"
        temperature = 25

        try:
            weather_type, temperature = get_weather(city)
        except Exception:
            pass

        cursor = db.cursor(dictionary=True)
        query = """
        SELECT *
        FROM outfits
        WHERE occasion=%s
        AND style=%s
        AND weather_type=%s
        LIMIT 1
        """

        cursor.execute(query, (occasion, style, weather_type))
        outfit = cursor.fetchone()

        return render_template(
            'result.html',
            outfit=outfit,
            image_filename=image_filename,
            skin_tone=skin_tone,
            weather_type=weather_type,
            temperature=temperature,
            city=city
        )

    return render_template('recommend.html')

if __name__ == '__main__':
    app.run(debug=True)
