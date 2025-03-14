# 📰 Fake News Detector & Misinformation Analyzer

## 📌 Overview

- This project is an AI-powered Fake News Detector and Misinformation Analyzer, designed to identify and prevent the spread of fake news in online communications. It includes a real-time chat application where messages are analyzed for authenticity, and users can query an AI system for verification.

## 🚀 Features

🔹 Landing Page (Django Backend)

    - User Authentication (Login & Signup)

    - About Section

    - Project Information

🔹 Chat Application (FastAPI Backend + WebSockets)

- Real-time messaging similar to WhatsApp

- Fake news detection with confidence level analysis

- Warning messages for detected fake news

- Users can query AI for more information on flagged messages

- Users can ask AI to verify doubtful messages

🔹 Analytics Dashboard (Django Backend)

    - Total messages analyzed

    - Fake vs. real message statistics

    - User interactions with AI

    - Insights on misinformation trends

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
