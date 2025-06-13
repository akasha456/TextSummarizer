import nltk
import numpy as np
import networkx as nx
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import warnings
from utils import preprocess_text, split_text_into_chunks
from config import ABSTRACTIVE_MODEL, ABSTRACTIVE_TOKENIZER, MAX_CHUNK_LENGTH, STOP_WORDS_LANGUAGE

warnings.filterwarnings('ignore')

# Initialize abstractive summarization model
@st.cache_resource
def load_abstractive_model():
    """Load and cache the abstractive summarization model"""
    summarizer = pipeline(
        "summarization", 
        model=ABSTRACTIVE_MODEL,
        tokenizer=ABSTRACTIVE_TOKENIZER
    )
    return summarizer

class TextRankSummarizer:
    """Extractive text summarization using TextRank algorithm"""
    
    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words(STOP_WORDS_LANGUAGE))
    
    def sentence_similarity(self, sent1, sent2):
        """Calculate similarity between two sentences using TF-IDF"""
        vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        try:
            tfidf_matrix = vectorizer.fit_transform([sent1, sent2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except:
            return 0.0
    
    def build_similarity_matrix(self, sentences):
        """Create similarity matrix for sentences"""
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    similarity_matrix[i][j] = self.sentence_similarity(sentences[i], sentences[j])
        
        return similarity_matrix
    
    def summarize(self, text, num_sentences=3):
        """Generate extractive summary using TextRank algorithm"""
        # Preprocess text
        text = preprocess_text(text)
        
        # Split into sentences
        sentences = nltk.sent_tokenize(text)
        
        if len(sentences) < 2:
            return text
        
        # Adjust number of sentences if text is short
        num_sentences = min(num_sentences, len(sentences))
        
        # Build similarity matrix
        similarity_matrix = self.build_similarity_matrix(sentences)
        
        # Apply PageRank algorithm
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph, max_iter=100, tol=1e-4)
        
        # Rank sentences
        ranked_sentences = sorted(((scores[i], s, i) for i, s in enumerate(sentences)), reverse=True)
        
        # Select top sentences and maintain original order
        selected_indices = sorted([ranked_sentences[i][2] for i in range(num_sentences)])
        summary_sentences = [sentences[i] for i in selected_indices]
        
        return ' '.join(summary_sentences)

def abstractive_summarize(text, max_length=150, min_length=50):
    """Generate abstractive summary using transformer model"""
    try:
        # Load the model
        summarizer = load_abstractive_model()
        
        # Handle long text by splitting into chunks
        if len(text.split()) > MAX_CHUNK_LENGTH:
            chunks = split_text_into_chunks(text, MAX_CHUNK_LENGTH)
            
            # Summarize each chunk
            chunk_summaries = []
            for chunk in chunks:
                summary = summarizer(
                    chunk, 
                    max_length=max_length//len(chunks), 
                    min_length=min_length//len(chunks), 
                    do_sample=False
                )
                chunk_summaries.append(summary[0]['summary_text'])
            
            # If multiple chunks, summarize the combined summaries
            if len(chunk_summaries) > 1:
                combined_summary = " ".join(chunk_summaries)
                final_summary = summarizer(
                    combined_summary, 
                    max_length=max_length, 
                    min_length=min_length, 
                    do_sample=False
                )
                return final_summary[0]['summary_text']
            else:
                return chunk_summaries[0]
        else:
            # Process normally for shorter text
            summary = summarizer(
                text, 
                max_length=max_length, 
                min_length=min_length, 
                do_sample=False
            )
            return summary[0]['summary_text']
    
    except Exception as e:
        st.error(f"Error in abstractive summarization: {str(e)}")
        return "Error generating summary. Please try with shorter text or check your input."