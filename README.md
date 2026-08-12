# StyleAI - AI Outfit Recommendation System

## Overview

StyleAI is an AI-powered fashion recommendation web application that helps users discover suitable outfits based on:

* Skin Tone Detection
* Current Weather Conditions
* Occasion Selection
* Style Preferences

The system analyzes user inputs and recommends personalized outfits from a curated fashion dataset.

---

## Features

### AI Skin Tone Detection

* Upload an image
* Automatically detects skin tone
* Supports Fair, Medium and Dark skin tones

### Weather-Based Recommendations

* Fetches live weather data using city name
* Classifies weather into:

  * Hot
  * Normal
  * Cold

### Occasion-Based Outfit Matching

Supports:

* College
* Office
* Interview
* Party

### Style Preferences

Supports:

* Casual
* Formal
* Smart Casual
* Business Casual
* Business Formal
* Smart Party
* Casual Party
* Formal Party
* Ethnic Party
* Wedding Ethnic
* Wedding

### Personalized Outfit Scoring

Recommendations are ranked based on:

* Occasion match
* Style match
* Weather suitability
* Skin tone suitability

### Favorite Outfits

* Save favorite outfits
* Stored using browser Local Storage
* Works without user login
* Favorites remain available on the same device

### Responsive Design

* Mobile Friendly
* Tablet Friendly
* Desktop Friendly

### Image Upload Support

* Mobile Gallery Upload
* Laptop/Desktop File Upload

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### Backend

* Python
* Flask

### Database

* SQLite

### AI & External Services

* OpenCV
* Weather API

---

## Project Structure

AI-Outfit-Recommender/

├── app.py

├── outfit_recommender.db

├── requirements.txt

├── README.md

├── services/

│ ├── skin_tone.py

│ └── weather_service.py

├── static/

│ ├── css/

│ ├── outfit_images/

│ └── uploads/

└── templates/

├── index.html

├── recommend.html

├── result.html

└── favorites.html

---

## Dataset

The system contains:

* 296+ outfit combinations
* Multiple style categories
* Occasion-specific outfits
* Weather-aware outfit mappings
* Skin tone compatibility information

---

## Installation

### Clone Repository

git clone <repository-url>

cd AI-Outfit-Recommender

### Create Virtual Environment

python -m venv venv

### Activate Environment

Windows:

venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Run Application

python app.py

---

## Usage

1. Open the application.
2. Upload your image.
3. Select occasion.
4. Choose preferred style (optional).
5. Enter city name.
6. Click "Discover Your Perfect Outfit".
7. View personalized recommendations.
8. Save outfits to favorites.

---

## Future Enhancements

* User Authentication
* User Profiles
* Outfit History
* Fashion Trend Analysis
* AI Color Matching
* Body Type Detection
* Recommendation Feedback System
* Admin Dashboard

---

## Author

Developed as an AI-powered outfit recommendation project using Flask, SQLite and Machine Learning concepts.
