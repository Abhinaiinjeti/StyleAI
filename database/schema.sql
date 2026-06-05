CREATE DATABASE IF NOT EXISTS outfit_recommender;

USE outfit_recommender;

CREATE TABLE outfits (
    id INT PRIMARY KEY AUTO_INCREMENT,
    occasion VARCHAR(50),
    style VARCHAR(50),
    weather_type VARCHAR(50),
    skin_tone VARCHAR(50),
    image_url VARCHAR(255),
    top_wear VARCHAR(100),
    bottom_wear VARCHAR(100),
    footwear VARCHAR(100),
    accessories VARCHAR(100)
);