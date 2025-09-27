# faq_chatbot.py

import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data (only first time)
nltk.download('punkt')

# Step 1: Collect FAQs (sample data)
faqs = {
    "What is your return policy?": "You can return any product within 30 days of purchase.",
    "How can I track my order?": "You can track your order using the tracking link sent to your email.",
    "What payment methods are accepted?": "We accept credit cards, debit cards, UPI, and PayPal.",
    "Do you offer international shipping?": "Yes, we ship internationally with additional charges.",
    "How can I contact customer support?": "You can reach our support team at support@example.com."
}

questions = list(faqs.keys())
answers = list(faqs.values())

# Step 2: Preprocess + TF-IDF Vectorization
vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english')
tfidf_matrix = vectorizer.fit_transform(questions)

def chatbot_response(user_input):
    # Transform user input
    user_tfidf = vectorizer.transform([user_input])
    
    # Compute cosine similarity
    similarities = cosine_similarity(user_tfidf, tfidf_matrix)
    index = np.argmax(similarities)
    
    # Best matching answer
    return answers[index]

# Simple chatbot loop
print("Chatbot: Hi! Ask me anything about our store. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    response = chatbot_response(user_input)
    print("Chatbot:", response)