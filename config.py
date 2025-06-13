# Configuration settings for Text Summarizer App

# Model Configuration
ABSTRACTIVE_MODEL = "facebook/bart-large-cnn"
ABSTRACTIVE_TOKENIZER = "facebook/bart-large-cnn"

# Default Parameters for Abstractive Summarization
DEFAULT_ABS_MAX_LENGTH = 150
DEFAULT_ABS_MIN_LENGTH = 50
ABS_MAX_RANGE = (50, 300)
ABS_MIN_RANGE = (20, 100)

# Default Parameters for Extractive Summarization
DEFAULT_NUM_SENTENCES = 3
NUM_SENTENCES_RANGE = (1, 10)

# Text Processing Configuration
MAX_CHUNK_LENGTH = 1024  # BART's maximum input length
STOP_WORDS_LANGUAGE = 'english'

# UI Configuration
PAGE_TITLE = "Advanced Text Summarizer"
PAGE_ICON = "📝"
LAYOUT = "wide"
MIN_WORD_COUNT_WARNING = 50

# Summarization Methods
SUMMARIZATION_METHODS = [
    "Abstractive (AI-Generated)",
    "Extractive (TextRank)", 
    "Both Methods"
]

# Input Methods
INPUT_METHODS = ["Type/Paste Text", "Sample Text"]

# NLTK Data Requirements
NLTK_REQUIREMENTS = [
    'punkt_tab',
    'punkt', 
    'stopwords'
]