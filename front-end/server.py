from flask import Flask
from flask_cors import CORS
from sklearn.externals import joblib
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
import nltk

st = PorterStemmer()
app = Flask(__name__)
CORS(app)

model = joblib.load('../SavedTopicModels/nmf500k_18topics')
'''tfidf = joblib.load('../SavedTopicModels/tfidf')'''
tfidf_vec = joblib.load('../SavedTopicModels/tfidf_vec2')

@app.route('/topic/<input>')
def topic(input):
    input_stemmed = []
    input_stemmed.append(" ".join([st.stem(i) for i in input.split()]))
    tfidf_input = tfidf_vec.transform(input_stemmed);
    topic_values = model.transform(tfidf_input);
    print(topic_values);

if __name__ == "__main__":
    app.run()
