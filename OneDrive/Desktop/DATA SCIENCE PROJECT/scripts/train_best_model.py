import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import os

def train_model():
    print("Loading data...")
    df = pd.read_csv('data/Restaurant_Reviews.tsv', delimiter='\t')
    
    # Preprocessing as seen in pythoncode.ipynb
    # (Removing punctuation is done there, but simpler is often better for consistency with app.py)
    # The app.py currently doesn't do heavy preprocessing, so I'll try to match what works best.
    
    X = df['Review']
    y = df['Liked']
    
    print("Vectorizing data...")
    vectorizer = CountVectorizer()
    X_count = vectorizer.fit_transform(X)
    
    print("Training Random Forest model (tuning via GridSearch)...")
    rf_model = RandomForestClassifier(random_state=17)
    
    rf_params = {
        "max_depth": [None],
        "max_features": [5, 7, "sqrt"],
        "min_samples_split": [2, 5],
        "n_estimators": [100, 200]
    }
    
    # Using a slightly reduced grid for speed, or just the best settings if known.
    # From notebook, None/auto/2/100 or 200 seemed to be in the search range.
    
    grid_search = GridSearchCV(rf_model, rf_params, cv=5, n_jobs=-1, verbose=1)
    grid_search.fit(X_count, y)
    
    best_model = grid_search.best_estimator_
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
    
    # Save the model and vectorizer
    os.makedirs('src/models', exist_ok=True)
    
    model_path = 'src/models/random_forest_model.pkl'
    vectorizer_path = 'src/models/rf_vectorizer.pkl'
    
    print(f"Saving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(best_model, f)
        
    print(f"Saving vectorizer to {vectorizer_path}...")
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("Success!")

if __name__ == "__main__":
    train_model()
