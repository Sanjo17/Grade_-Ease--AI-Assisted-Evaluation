import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, top_n=5):

    if text == '':
        return "null"
    # Tokenization
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    # Convert tokens back to a single string
    processed_text = ' '.join(stemmed_tokens)

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_text])

    # Get feature names (i.e., words)
    feature_names = vectorizer.get_feature_names_out()

    # Extract top N keywords based on TF-IDF scores
    top_indices = tfidf_matrix.toarray().argsort()[0][::-1][:top_n]
    top_keywords = [feature_names[idx] for idx in top_indices]

    return top_keywords
    
def count_words(answer):
    words = answer.split()
    # Count the number of words
    word_count = len(words)
    return word_count
# Example usage:
# text = ""
# keywords = extract_keywords(text)
# print("Top keywords:", keywords)

