from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample corpus
documents = [
    "This is a sample document.",
    "This document is another example.",
    "TF-IDF is a statistical measure."
]

# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the documents
tfidf_matrix = vectorizer.fit_transform(documents)

# Define a query
query = ["example document"]

# Transform the query
query_vec = vectorizer.transform(query)

# Compute cosine similarity
cosine_sim = cosine_similarity(query_vec, tfidf_matrix)

# Get the most relevant document index
most_relevant_idx = np.argmax(cosine_sim)

# Retrieve the most relevant document
most_relevant_doc = documents[most_relevant_idx]

print(f"Most relevant document: {most_relevant_doc}")

# Use the most relevant document as context for a generation model
# (Assuming you have a function generate_response that takes a context)
# response = generate_response(context=most_relevant_doc)
