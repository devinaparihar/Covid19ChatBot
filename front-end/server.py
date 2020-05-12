from flask import Flask, Response
from flask_cors import CORS
from googlesearch import search
import numpy as np
from sklearn.externals import joblib
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
import nltk
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text

st = PorterStemmer()
app = Flask(__name__)
CORS(app)

model = joblib.load('../SavedTopicModels/nmf500kstemmed_14topics')
tfidf_vec = joblib.load('../SavedTopicModels/tfidf_vec2stemmed14topics')

topics = ["Cases", "Spreading/Getting", "Death Toll", "n/a", "Protection/Masks",
    "n/a", "n/a", "n/a", "Racism/Xenophobia", "Outbreak Origin", "n/a",
    "Cruise Ships/dog", "n/a", "america/US/president"]

data = pd.read_excel("Chatbot_qa.xlsx", encoding='utf8')
module = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')

def respond_highest_scoring_answer(question, label):


  # will need to get the data as a dataframe beforehand or sometime here
  filtered_data = data.loc[data[label] == 1, ['Context', 'Answer']].reset_index(drop=True)
  response_encodings = module.signatures['response_encoder'](
        input=tf.constant(filtered_data.Answer),
        context=tf.constant(filtered_data.Context))['outputs']

  question_encodings = module.signatures['question_encoder'](
    tf.constant(question)
  )['outputs']
  qa_inner_prods = np.inner(question_encodings, response_encodings)
  qa_array = qa_inner_prods[0]
  return filtered_data.Answer[np.argmax(qa_inner_prods, axis=1)].values[0]

def show_top_5_questions(question, label):

    #data = pd.read_excel("Chatbot_qa.xlsx", encoding='utf8')
    #module = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')

    # will need to get the data as a dataframe beforehand or sometime here
    filtered_data = data.loc[data[label] == 1, ['Context', 'Answer']].reset_index(drop=True)
    response_encodings = module.signatures['response_encoder'](
          input=tf.constant(filtered_data.Answer),
          context=tf.constant(filtered_data.Context))['outputs']

    question_encodings = module.signatures['question_encoder'](
      tf.constant(question)
    )['outputs']
    qa_inner_prods = np.inner(question_encodings, response_encodings)
    qa_array = qa_inner_prods[0]

    N = 5

    top_N_response_indices = np.argpartition(qa_array, -N)[-N:]
    sorted_top_response_indicies = top_N_response_indices[np.argsort(qa_array[top_N_response_indices])[::-1][:N]]
    top_possible_questions = pd.Series.to_numpy(filtered_data.Context[sorted_top_response_indicies])
    top_possible_questions = np.insert(top_possible_questions, N, 'None of the above questions are similar to what I asked')

    frame = {'Which is your question?': top_possible_questions}
    questions_df = pd.DataFrame(frame, index=np.arange(1, N+2, 1))

    return '<br><br>'.join(questions_df['Which is your question?'].values)


@app.route('/topic/load')
def load():
    print("test")
    return Response(status = 200)

@app.route('/topic/<input>')
def topic(input):

    input_stemmed = []
    input_stemmed.append(" ".join([st.stem(i) for i in input.split()]))
    tfidf_input = tfidf_vec.transform(input_stemmed);
    topic_values = model.transform(tfidf_input);
    topic_preds = topic_values.tolist()[0]
    max = 0;
    for x in range(1, 14):
        if x == 3 or x == 6 or x == 7 or x == 10 or x == 12:
            continue;
        if topic_preds[x] > topic_preds[max]:
            max = x;
    if topic_preds[max] == 0:
        return "We're sorry, we couldn't answer that question"
        #prompt a google search
    elif max == 11:
        return "You're asking a question related to " + "Cruise Ships / dog" + "; is that correct?"
    else:
        print(topics[max])
        return respond_highest_scoring_answer(input, topics[max])

@app.route('/topic/topfivequestions/<input>')
def topfivequestions(input):
    print("show top 5 questions")
    input_stemmed = []
    input_stemmed.append(" ".join([st.stem(i) for i in input.split()]))
    tfidf_input = tfidf_vec.transform(input_stemmed);
    topic_values = model.transform(tfidf_input);
    topic_preds = topic_values.tolist()[0]
    max=0;
    for x in range(1, 14):
        if x == 3 or x == 6 or x == 7 or x == 10 or x == 12:
            continue;
        if topic_preds[x] > topic_preds[max]:
            max = x;
    ret = show_top_5_questions(input, topics[max])
    print(ret);

    return str(ret);

@app.route('/onlinesearch/<input>')
def onlinesearch(input):
  search_result_list = list(search(input, tld="com", num=10, stop=3, pause=1))
  ret = "<a href='" + search_result_list[0] + "' target='_blank'>"+search_result_list[0]+"</a>"
  return ret

@app.route('/getanswer/<question>')
def getanswer(question):
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(data.head())
    #print(data[data['Context']==question])
    print(question+"?");
    print(data[data['Context'] == question + "?"])
    #print(data[data['Context'] == question + "?"].Answer.tolist()[0])
    #print(data.loc[[question],['Answer']])
    #print("lastly: " + str(data[data['Context'] == question].index[0]))
    return data[data['Context'] == question + "?"].Answer.tolist()[0]


#if __name__ == "__main__":
#    app.run()
