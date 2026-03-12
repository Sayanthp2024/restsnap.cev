import pandas as pd
import pickle
import os
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

def evaluate_models():
    # Load data
    data_path = 'data/Restaurant_Reviews.tsv'
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}")
        return
    
    df = pd.read_csv(data_path, delimiter='\t')
    X = df['Review']
    y = df['Liked']
    
    # Load vectorizer
    vectorizer_path = 'src/models/tfidf_vectorizer.pkl'
    if not os.path.exists(vectorizer_path):
        print(f"Vectorizer not found at {vectorizer_path}")
        return
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer_tfidf = pickle.load(f)
    
    # Load RF vectorizer
    rf_vectorizer_path = 'src/models/rf_vectorizer.pkl'
    if os.path.exists(rf_vectorizer_path):
        with open(rf_vectorizer_path, 'rb') as f:
            vectorizer_rf = pickle.load(f)
    else:
        vectorizer_rf = None
    
    models = {
        'sentiment_model.pkl (Logistic)': {'path': 'src/models/sentiment_model.pkl', 'vec': vectorizer_tfidf},
        'naive_bayes_model.pkl (MultinomialNB)': {'path': 'src/models/naive_bayes_model.pkl', 'vec': vectorizer_tfidf},
        'random_forest_model.pkl (RF)': {'path': 'src/models/random_forest_model.pkl', 'vec': vectorizer_rf}
    }
    
    for name, info in models.items():
        path = info['path']
        vec = info['vec']
        if os.path.exists(path) and vec:
            with open(path, 'rb') as f:
                model = pickle.load(f)
            try:
                X_transformed = vec.transform(X)
                y_pred = model.predict(X_transformed)
                acc = accuracy_score(y, y_pred)
                print(f"Model: {name}, Accuracy: {acc:.4f}")
            except Exception as e:
                print(f"Error evaluating {name}: {e}")

if __name__ == "__main__":
    evaluate_models()
