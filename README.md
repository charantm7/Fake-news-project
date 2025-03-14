# 📰 Fake News Detector & Misinformation Analyzer

## 📌 Overview

- This project is an AI-powered Fake News Detector and Misinformation Analyzer, designed to identify and prevent the spread of fake news in online communications. It includes a real-time chat application where messages are analyzed for authenticity, and users can query an AI system for verification.

## 🚀 Features

### 🔹 Landing Page (Django Backend)

- User Authentication (Login & Signup)

- About Section

- Project Information

### 🔹 Chat Application (FastAPI Backend + WebSockets)

- Real-time messaging similar to WhatsApp

- Fake news detection with confidence level analysis

- Warning messages for detected fake news

- Users can query AI for more information on flagged messages

- Users can ask AI to verify doubtful messages

### 🔹 Analytics Dashboard (Django Backend)

- Total messages analyzed

- Fake vs. real message statistics

- User interactions with AI

- Insights on misinformation trends

## ⚙️ Technologies Used

- Backend: Django, FastAPI, WebSockets
  
- Frontend: HTML, CSS, JavaScript
  
- Database: PostgreSQL
  
- AI Model: NLP-based Fake News Detection

## 🔧 Setup & Installation

### Clone the Repository

    - git clone https://github.com/charantm7/Fake-news-project.git
    
    - cd Fake-news-project
    
### Backend Setup (Django)

    - python3 -m venv venv
    
    - source venv/bin/activate
    
    - pip install -r requirements.txt
    
    - cd backend
    
    - python manage.py migrate
    
    - python manage.py runserver
### Chat Backend Setup (FastAPI)

    - cd chat_app

    - uvicorn main:app --reload
    
## 🏗️ Project Structure

- Fake-news-project/
- |── ai_model/
- | ├── inference.py
- | ├── model.py
- │── backend/ (Django Backend for Landing Page & Dashboard)
- │ ├── manage.py
- │ ├── authentication
- | ├── dashboard
- │ ├── core/
- │ │ ├── settings.py
- │ │ ├── urls.py
- │ │ ├── wsgi.py
- │── chat_app/ (FastAPI Backend for Chat & WebSockets)
- │ ├── main.py
- │ ├── models.py
- │ ├── websocket.py
- │── frontend/ (Frontend UI for Chat & Landing Page)
- | ├── templates/
- | | ├── templates/
- | | | ├── landing/
- | | | | ├── index.html
- | | | ├── chat/
- | | | ├── dashboard/
- │ ├── static/
- │ | ├── css/
- | | ├── js/
- │ | ├── assets/
- │── README.md

## 📜 License

- This project is licensed under the GNU General Public License v3.0.
  

### 🚀 Developed for Hackathon 2025 by Team SYNDICATES! 🎯
