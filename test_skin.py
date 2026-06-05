from services.skin_tone import detect_skin_tone

result = detect_skin_tone(
    "static/uploads/Abhi.jpeg"
)

print(result)