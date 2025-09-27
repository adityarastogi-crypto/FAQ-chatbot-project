from flask import Flask, render_template, request, jsonify
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import preprocess

app = Flask(__name__)

# Load FAQs
with open('faqs.json', 'r', encoding='utf-8') as f:
    faqs = json.load(f)

# Preprocess FAQ questions and fit TF-IDF
faq_questions = [preprocess(item['question']) for item in faqs]
vectorizer = TfidfVectorizer()
if any(faq_questions):
    X_faq = vectorizer.fit_transform(faq_questions)
else:
    X_faq = vectorizer.fit_transform([""])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    payload = request.get_json(force=True)
    question = payload.get('question', '').strip()
    if not question:
        return jsonify({'answer': "Please type a question."})

    q_proc = preprocess(question)
    q_vec = vectorizer.transform([q_proc])
    sims = cosine_similarity(q_vec, X_faq)[0]
    best_idx = int(sims.argmax())
    score = float(sims[best_idx])

    # threshold: tune as needed (0.25 is conservative)
    if score < 0.25:
        return jsonify({
            'answer': "Sorry, I couldn't find a confident answer. Try rephrasing your question.",
            'score': score
        })

    return jsonify({
        'answer': faqs[best_idx]['answer'],
        'score': score
    })

if __name__ == '__main__':
    # debug=True auto reloads on file save (useful in development)
    app.run(host='127.0.0.1', port=5000, debug=True)
