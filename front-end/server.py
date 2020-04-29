from flask import Flask
from flask_cors import CORS
from sklearn.externals import joblib
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

app = Flask(__name__)
CORS(app)

model = joblib.load('../SavedTopicModels/nmf500k_18topics')
'''tfidf = joblib.load('../SavedTopicModels/tfidf')'''
tfidf_vec = joblib.load('../tfidf_vec2')

@app.route('/topic/<input>')
def topic(input):
    tfidf_input = tfidf_vec.transform([input]);
    topic_values = model.transform(tfidf_input);
    print(topic_values);

if __name__ == "__main__":
    app.run()
