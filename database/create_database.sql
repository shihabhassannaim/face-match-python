CREATE DATABASE SomalilandNID;

USE SomalilandNID;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    nid_number VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255),
    passport_image VARCHAR(255),
    video_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
