import pandas as pd
import joblib
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

data = pd.read_csv("dataset/UpdatedResumeDataSet.csv")

def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]',' ',text)
    return text.lower()

data["Resume"] = data["Resume"].apply(clean_text)

X = data["Resume"]
y = data["Category"]

vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1,2),
    max_features=5000
)

X_vec = vectorizer.fit_transform(X)

model = LinearSVC()
model.fit(X_vec,y)

joblib.dump(model,"model/resume_model.pkl")
joblib.dump(vectorizer,"model/vectorizer.pkl")

print("High Accuracy Resume Model Ready")
