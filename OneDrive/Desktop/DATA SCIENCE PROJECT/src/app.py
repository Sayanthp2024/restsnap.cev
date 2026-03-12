from flask import Flask, request, jsonify, render_template
import os
import pickle
import numpy as np
import re

app = Flask(__name__)

# Get path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load trained model
model = pickle.load(open(os.path.join(MODEL_DIR, "random_forest_model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(MODEL_DIR, "rf_vectorizer.pkl"), "rb"))

# Aspect Keywords
ASPECTS = {
    "food": ["food", "meal", "dish", "taste", "flavor", "delicious", "menu", "pasta", "pizza", "ingredients", "tasty", "yummy", "cooking", "cuisine", "breakfast", "lunch", "dinner", "dessert", "appetizer"],
    "service": ["service", "waiter", "staff", "manager", "attentive", "slow", "fast", "friendly", "rude", "wait", "server", "waitress", "hospitality", "hostess", "host", "behavior", "order", "delivery"],
    "ambience": ["ambience", "atmosphere", "decor", "music", "seating", "lighting", "cozy", "noisy", "place", "interior", "setting", "vibe", "clean", "design", "quiet", "view"],
    "price": ["price", "cost", "value", "expensive", "cheap", "bill", "worth", "money", "affordable", "pricing", "budget", "wallet", "pricy", "overpriced", "fair", "deal", "receipt", "check"]
}

# In-memory storage for session data
session_reviews = []
aspect_stats = {
    "food": {"pos": 0, "neg": 0},
    "service": {"pos": 0, "neg": 0},
    "ambience": {"pos": 0, "neg": 0},
    "price": {"pos": 0, "neg": 0}
}

@app.route("/")
def home():
    return render_template("index.html")

# Sentiment Lexicon for Aspect Boosting
POS_WORDS = {"great", "good", "excellent", "amazing", "wonderful", "fair", "affordable", "fast", "quick", "friendly", "attentive", "nice", "loved", "delicious", "tasty"}
NEG_WORDS = {"bad", "terrible", "horrible", "awful", "slow", "expensive", "rude", "poor", "overpriced", "disappointing", "bland", "cold"}

def get_aspect_sentiment(text):
    results = {}
    fragments = re.split(r'[,.!\?;]|\band\b', text.lower())
    
    for aspect, keywords in ASPECTS.items():
        aspect_fragments = []
        for frag in fragments:
            if any(kw in frag for kw in keywords):
                aspect_fragments.append(frag.strip())
        
        if aspect_fragments:
            frag_text = " ".join(aspect_fragments)
            vec = vectorizer.transform([frag_text])
            pred = model.predict(vec)[0]
            
            # Simple Lexicon Boost for short fragments
            words = set(frag_text.split())
            pos_hits = len(words.intersection(POS_WORDS))
            neg_hits = len(words.intersection(NEG_WORDS))
            
            if pos_hits > neg_hits:
                pred = 1
            elif neg_hits > pos_hits:
                pred = 0
                
            sentiment = "positive" if pred == 1 else "negative"
            results[aspect] = sentiment
            
            # Update session stats
            sentiment_key = "pos" if pred == 1 else "neg"
            aspect_stats[aspect][sentiment_key] += 1
            
    return results

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    review = data["review"]
    
    session_reviews.append(review)
    review_vector = vectorizer.transform([review])

    prediction = model.predict(review_vector)[0]
    probabilities = model.predict_proba(review_vector)[0]
    confidence = float(np.max(probabilities))

    aspects = get_aspect_sentiment(review)
    result = "liked" if prediction == 1 else "disliked"

    return jsonify({
        "prediction": result,
        "confidence": confidence,
        "aspects": aspects
    })

@app.route("/aspect_stats", methods=["GET"])
def get_stats():
    # Calculate positive percentage for each aspect
    output = {}
    for aspect, counts in aspect_stats.items():
        total = counts["pos"] + counts["neg"]
        percent = (counts["pos"] / total * 100) if total > 0 else 0
        output[aspect] = {
            "percent": round(percent, 1),
            "total": total
        }
    return jsonify(output)

@app.route("/summarize", methods=["POST"])
def summarize():
    if not session_reviews:
        return jsonify({"summary": "No reviews analyzed yet."})
    
    # Simple extractive summarization: 
    # For a small demo, we provide a concise join of unique highlights.
    unique_reviews = list(set(session_reviews))
    if len(unique_reviews) > 3:
        summary = "Based on recent feedback: " + "; ".join(unique_reviews[-3:]) + " (and more...)"
    else:
        summary = "Summing up: " + " | ".join(unique_reviews)
        
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)