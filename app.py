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
        style = request.form.get('style', '')
        city = request.form['city']

        image = request.files.get('image')
        image_filename = ""
        skin_tone = "Medium"

        if image and image.filename:
            image_filename = image.filename
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                image_filename
            )
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

        # ---------------------------------
        # Flexible matching rules
        # ---------------------------------

        weather_map = {
            "Hot": ["Hot", "Normal"],
            "Normal": ["Hot", "Normal", "Cold"],
            "Cold": ["Cold", "Normal"]
        }

        skin_map = {
            "Fair": ["Fair", "Medium"],
            "Medium": ["Fair", "Medium", "Dark"],
            "Dark": ["Medium", "Dark"]
        }

        valid_weather = weather_map.get(weather_type, [weather_type])
        valid_skin = skin_map.get(skin_tone, [skin_tone])

        all_outfits = []
        seen_ids = set()

        # ------------------------------
        # Query 1: Exact style match
        # ------------------------------

        if style:

            query1 = f"""
            SELECT *
            FROM outfits
            WHERE occasion=?
            AND style=?
            AND weather_type IN ({','.join(['?'] * len(valid_weather))})
            AND skin_tone IN ({','.join(['?'] * len(valid_skin))})
            ORDER BY RANDOM()
            LIMIT 12
            """

            params1 = [occasion, style] + valid_weather + valid_skin

        else:

            query1 = f"""
            SELECT *
            FROM outfits
            WHERE occasion=?
            AND weather_type IN ({','.join(['?'] * len(valid_weather))})
            AND skin_tone IN ({','.join(['?'] * len(valid_skin))})
            ORDER BY RANDOM()
            LIMIT 12
            """

            params1 = [occasion] + valid_weather + valid_skin

        cursor.execute(query1, params1)

        for row in cursor.fetchall():
            if row["id"] not in seen_ids:
                all_outfits.append(dict(row))
                seen_ids.add(row["id"])
        # ------------------------------
        # Query 2: Ignore style
        # ------------------------------

        if len(all_outfits) < 8:

            query2 = f"""
            SELECT *
            FROM outfits
            WHERE occasion=?
            AND weather_type IN ({','.join(['?'] * len(valid_weather))})
            AND skin_tone IN ({','.join(['?'] * len(valid_skin))})
            ORDER BY RANDOM()
            LIMIT 20
            """

            params2 = [occasion] + valid_weather + valid_skin

            cursor.execute(query2, params2)

            for row in cursor.fetchall():
                if row["id"] not in seen_ids:
                    all_outfits.append(dict(row))
                    seen_ids.add(row["id"])

                    if len(all_outfits) >= 8:
                        break

        # ------------------------------
        # Query 3: Occasion only
        # ------------------------------

        if len(all_outfits) < 8:

            cursor.execute("""
                SELECT *
                FROM outfits
                WHERE occasion=?
                ORDER BY RANDOM()
                LIMIT 30
            """, (occasion,))

            for row in cursor.fetchall():
                if row["id"] not in seen_ids:
                    all_outfits.append(dict(row))
                    seen_ids.add(row["id"])

                    if len(all_outfits) >= 8:
                        break

        for outfit in all_outfits:

            score = 60

            if outfit["occasion"] == occasion:
                score += 15

            if outfit["weather_type"] in valid_weather:
                score += 15

            if outfit["skin_tone"] in valid_skin:
                score += 10

            if style and outfit["style"] == style:
                score += 10

            outfit["match_score"] = min(score, 100)

        outfits = sorted(
        all_outfits,
        key=lambda x: x["match_score"],
        reverse=True
        )[:20]

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