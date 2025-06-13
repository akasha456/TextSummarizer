import nltk
import streamlit as st
import re
from config import NLTK_REQUIREMENTS

# Download required NLTK data
@st.cache_resource
def download_nltk_data():
    """Download required NLTK data for text processing"""
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

def preprocess_text(text):
    """Clean and preprocess text by removing extra whitespaces and normalizing"""
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def calculate_compression_ratio(original_text, summary):
    """Calculate compression ratio between original text and summary"""
    original_words = len(original_text.split())
    summary_words = len(summary.split())
    if original_words == 0:
        return 0
    return round((1 - summary_words / original_words) * 100, 2)

def split_text_into_chunks(text, max_chunk_length=1024):
    """Split long text into smaller chunks for processing"""
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len((current_chunk + " " + sentence).split()) <= max_chunk_length:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def get_word_count(text):
    """Get word count of text"""
    return len(text.split())

def validate_text_input(text, min_words=50):
    """Validate if text input meets minimum requirements"""
    if not text.strip():
        return False, "Please enter some text to summarize."
    
    word_count = get_word_count(text)
    if word_count < min_words:
        return True, f"⚠️ For best results, please provide text with at least {min_words} words. Current: {word_count} words."
    
    return True, f"📊 Word count: {word_count}"