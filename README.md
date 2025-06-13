# Advanced Text Summarizer

A professional-grade text summarization application built with Streamlit and state-of-the-art NLP techniques. This app provides both extractive and abstractive summarization methods to generate high-quality summaries from any text input.

## 🌟 Features

### Dual Summarization Methods
- **Abstractive Summarization**: Uses Facebook's BART model to generate new, coherent summaries
- **Extractive Summarization**: Implements TextRank algorithm to select and rank important sentences
- **Comparison Mode**: View both methods side-by-side for comprehensive analysis

### Advanced NLP Implementation
- Custom TextRank implementation using TF-IDF vectorization and cosine similarity
- NetworkX integration for PageRank algorithm application
- Intelligent text chunking for processing long documents
- Comprehensive text preprocessing and normalization

### Interactive Features
- Configurable parameters for both summarization methods
- Built-in sample texts for quick testing
- Real-time word counting and input validation
- Compression ratio metrics to measure summary efficiency
- Clean, responsive UI with progress indicators

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/akasha456/TextSummarizer-NLP-based-Text-Summarization-Tool
cd text-summarizer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

## 📁 Project Structure

```
text-summarizer/
├── app.py              # Main Streamlit application
├── summarizers.py      # Summarization classes and functions
├── utils.py           # Utility functions for text processing
├── config.py          # Configuration settings and constants
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## 🛠️ Usage

### Basic Usage
1. Launch the app using `streamlit run app.py`
2. Choose your input method (Type/Paste or Sample Text)
3. Configure summarization settings in the sidebar
4. Click "Generate Summary" to process your text

### Configuration Options

#### Abstractive Summarization
- **Max Summary Length**: 50-300 words (default: 150)
- **Min Summary Length**: 20-100 words (default: 50)

#### Extractive Summarization
- **Number of Sentences**: 1-10 sentences (default: 3)

### Summarization Methods

#### 🤖 Abstractive Summarization
- Uses BART (Bidirectional and Auto-Regressive Transformers)
- Generates new sentences that capture the essence of the original text
- Better at creating coherent, human-like summaries
- May introduce information not explicitly stated in the source

#### 🔗 Extractive Summarization
- Uses TextRank algorithm (similar to PageRank)
- Selects and ranks existing sentences from the original text
- Preserves original wording and factual accuracy
- Creates summaries by combining the most important sentences

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Transformers**: Hugging Face transformers for BART model
- **PyTorch**: Deep learning framework
- **NLTK**: Natural language processing toolkit
- **scikit-learn**: Machine learning library for TF-IDF
- **NetworkX**: Graph algorithms for PageRank
- **NumPy**: Numerical computing

### Model Information
- **Abstractive Model**: `facebook/bart-large-cnn`
- **Text Processing**: NLTK with punkt tokenizer and stopwords
- **Similarity Calculation**: TF-IDF with cosine similarity
- **Ranking Algorithm**: PageRank via NetworkX

## 🚀 Performance Features

- **Caching**: Model loading and NLTK data downloads are cached for faster subsequent runs
- **Chunking**: Long texts are intelligently split and processed in chunks
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Validation**: Input validation with helpful feedback

## 🔍 Sample Texts

The app includes built-in sample texts for testing:
- **Technology Article**: AI and machine learning overview
- **Scientific Research**: Climate change research summary

## 📊 Metrics

- **Compression Ratio**: Percentage reduction from original text to summary
- **Word Count**: Real-time word counting for input validation
- **Processing Time**: Visual feedback during summary generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Hugging Face for the BART model and Transformers library
- Facebook AI Research for the BART architecture
- NetworkX team for graph algorithms
- Streamlit team for the amazing web framework

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub or contact the maintainers.

---

**Built with ❤️ using Python, Streamlit, and modern NLP techniques**
