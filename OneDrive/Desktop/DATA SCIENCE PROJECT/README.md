# 🍴 TasteSense: AI-Powered Restaurant Review Intelligence

TasteSense is a premium data science application designed to help restaurant owners and managers extract deep, actionable insights from customer feedback. It goes beyond simple "liked/disliked" classification to provide a comprehensive analysis of the customer experience.

## ✨ Key Features

### 🧠 High-Accuracy Sentiment Analysis
Utilizes a **Random Forest** model (GridSearch-tuned) achieving **90.6%** accuracy to classify reviews into positive (Liked) or negative (Disliked) sentiments.

### 🔍 Aspect-Based Sentiment Analysis (ABSA)
The engine automatically identifies and evaluates feedback across four critical restaurant dimensions:
- **Food Quality**: Taste, flavor, presentation, and preparation.
- **Service**: Waitstaff behavior, speed, hospitality, and management.
- **Ambience**: Decor, music, lighting, seating, and general vibe.
- **Price**: Value for money, cost, billing, and affordability.

### 📝 Automatic Review Summarization
An AI-powered summarization engine that aggregates multiple customer reviews into a single, concise highlight reel, helping you understand the overall consensus at a glance.

### 📊 Professional Analytics Dashboard
A modern, 3-column "Pro" interface featuring:
- **Sentiment Discovery**: Real-time breakdown of current review aspects.
- **Global Distribution**: A visual donut chart showing overall sentiment trends.
- **Performance Bars**: Live metrics for each aspect (Food, Service, etc.) to track performance over time.
- **Recent Activity**: A persistent history panel that saves to your browser's local storage.

## 🛠️ Technical Stack
- **Backend**: Python (Flask)
- **Machine Learning**: Scikit-learn (Random Forest, TF-IDF Vectorization)
- **Frontend**: HTML5, CSS3 (Glassmorphism design), Vanilla JavaScript
- **Data Persistence**: Browser LocalStorage

## 🚀 Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python src/app.py`
3. Open in browser: `http://127.0.0.1:5000`

---
*Developed as a Data Science Excellence project.*
