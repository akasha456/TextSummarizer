import streamlit as st
from summarizers import TextRankSummarizer, abstractive_summarize
from utils import download_nltk_data, calculate_compression_ratio, get_word_count, validate_text_input
from config import (
    PAGE_TITLE, PAGE_ICON, LAYOUT, SUMMARIZATION_METHODS, INPUT_METHODS,
    DEFAULT_ABS_MAX_LENGTH, DEFAULT_ABS_MIN_LENGTH, ABS_MAX_RANGE, ABS_MIN_RANGE,
    DEFAULT_NUM_SENTENCES, NUM_SENTENCES_RANGE, MIN_WORD_COUNT_WARNING
)

def get_sample_texts():
    """Sample texts for testing the application"""
    return {
        "Technology Article": """
        Artificial Intelligence has revolutionized numerous industries in recent years, transforming how businesses operate and deliver services. Machine learning algorithms now power recommendation systems, autonomous vehicles, and medical diagnosis tools. The rapid advancement in deep learning has enabled computers to process natural language, recognize images, and make decisions with unprecedented accuracy. Companies are investing billions in AI research and development, recognizing its potential to drive innovation and competitive advantage. However, the widespread adoption of AI also raises important questions about job displacement, privacy, and ethical considerations. As AI systems become more sophisticated, there is growing debate about the need for regulation and oversight to ensure responsible development and deployment. The future of AI promises even greater integration into daily life, with smart homes, personalized healthcare, and intelligent transportation systems becoming increasingly common.
        """,
        "Scientific Research": """
        Climate change represents one of the most pressing challenges of our time, with far-reaching implications for global ecosystems and human societies. Rising global temperatures have led to melting ice caps, rising sea levels, and more frequent extreme weather events. Scientific evidence overwhelmingly supports the conclusion that human activities, particularly the burning of fossil fuels, are the primary drivers of current climate change. The Intergovernmental Panel on Climate Change has warned that without immediate and drastic action to reduce greenhouse gas emissions, the world faces catastrophic consequences. Renewable energy technologies, such as solar and wind power, have become increasingly cost-effective and are being deployed at scale worldwide. Governments, businesses, and individuals must work together to implement sustainable practices and transition to clean energy sources to mitigate the worst effects of climate change.
        """
    }

def setup_sidebar():
    """Configure the sidebar with summarization settings"""
    st.sidebar.header("⚙️ Configuration")
    
    summarization_type = st.sidebar.selectbox(
        "Summarization Method",
        SUMMARIZATION_METHODS
    )
    
    abs_settings = {}
    ext_settings = {}
    
    if summarization_type in ["Abstractive (AI-Generated)", "Both Methods"]:
        st.sidebar.subheader("Abstractive Settings")
        abs_settings['max_length'] = st.sidebar.slider(
            "Max Summary Length (words)", 
            ABS_MAX_RANGE[0], ABS_MAX_RANGE[1], 
            DEFAULT_ABS_MAX_LENGTH
        )
        abs_settings['min_length'] = st.sidebar.slider(
            "Min Summary Length (words)", 
            ABS_MIN_RANGE[0], ABS_MIN_RANGE[1], 
            DEFAULT_ABS_MIN_LENGTH
        )
    
    if summarization_type in ["Extractive (TextRank)", "Both Methods"]:
        st.sidebar.subheader("Extractive Settings")
        ext_settings['num_sentences'] = st.sidebar.slider(
            "Number of Sentences", 
            NUM_SENTENCES_RANGE[0], NUM_SENTENCES_RANGE[1], 
            DEFAULT_NUM_SENTENCES
        )
    
    return summarization_type, abs_settings, ext_settings

def setup_input_section():
    """Setup the input section of the application"""
    st.header("📄 Input Text")
    
    # Text input options
    input_method = st.radio("Input Method", INPUT_METHODS)
    
    if input_method == "Sample Text":
        sample_texts = get_sample_texts()
        selected_sample = st.selectbox("Choose Sample Text", list(sample_texts.keys()))
        input_text = st.text_area(
            "Text to Summarize", 
            sample_texts[selected_sample], 
            height=300
        )
    else:
        input_text = st.text_area(
            "Enter your text here", 
            height=300, 
            placeholder="Paste or type the text you want to summarize..."
        )
    
    # Display word count and validation
    is_valid, message = validate_text_input(input_text, MIN_WORD_COUNT_WARNING)
    
    if is_valid:
        if "⚠️" in message:
            st.warning(message)
        else:
            st.info(message)
    else:
        st.error(message)
    
    return input_text, is_valid

def display_summary_results(input_text, summarization_type, abs_settings, ext_settings):
    """Display summary results based on selected method"""
    
    if summarization_type == "Abstractive (AI-Generated)":
        summary = abstractive_summarize(
            input_text, 
            abs_settings['max_length'], 
            abs_settings['min_length']
        )
        
        st.subheader("🤖 Abstractive Summary")
        st.write(summary)
        
        compression = calculate_compression_ratio(input_text, summary)
        st.metric("Compression Ratio", f"{compression}%")
        
    elif summarization_type == "Extractive (TextRank)":
        textrank_summarizer = TextRankSummarizer()
        summary = textrank_summarizer.summarize(
            input_text, 
            ext_settings['num_sentences']
        )
        
        st.subheader("🔗 Extractive Summary")
        st.write(summary)
        
        compression = calculate_compression_ratio(input_text, summary)
        st.metric("Compression Ratio", f"{compression}%")
        
    else:  # Both methods
        col_abs, col_ext = st.columns(2)
        
        with col_abs:
            st.subheader("🤖 Abstractive")
            abs_summary = abstractive_summarize(
                input_text, 
                abs_settings['max_length'], 
                abs_settings['min_length']
            )
            st.write(abs_summary)
            abs_compression = calculate_compression_ratio(input_text, abs_summary)
            st.metric("Compression", f"{abs_compression}%")
        
        with col_ext:
            st.subheader("🔗 Extractive")
            textrank_summarizer = TextRankSummarizer()
            ext_summary = textrank_summarizer.summarize(
                input_text, 
                ext_settings['num_sentences']
            )
            st.write(ext_summary)
            ext_compression = calculate_compression_ratio(input_text, ext_summary)
            st.metric("Compression", f"{ext_compression}%")

def display_method_info():
    """Display information about summarization methods"""
    st.markdown("---")
    st.header("ℹ️ About the Methods")
    
    method_col1, method_col2 = st.columns(2)
    
    with method_col1:
        st.subheader("🤖 Abstractive Summarization")
        st.markdown("""
        - Uses **BART** (Bidirectional and Auto-Regressive Transformers)
        - Generates new sentences that capture the essence of the original text
        - Better at creating coherent, human-like summaries
        - May introduce information not explicitly stated in the source
        """)
    
    with method_col2:
        st.subheader("🔗 Extractive Summarization")
        st.markdown("""
        - Uses **TextRank** algorithm (similar to PageRank)
        - Selects and ranks existing sentences from the original text
        - Preserves original wording and factual accuracy
        - Creates summaries by combining the most important sentences
        """)

def main():
    """Main application function"""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT
    )
    
    st.title("🔍 Advanced Text Summarizer")
    st.markdown("Generate high-quality summaries using state-of-the-art NLP techniques")
    
    # Download NLTK data
    download_nltk_data()
    
    # Setup sidebar configuration
    summarization_type, abs_settings, ext_settings = setup_sidebar()
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        input_text, is_valid = setup_input_section()
    
    with col2:
        st.header("📋 Summary Results")
        
        if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
            if input_text.strip() and is_valid:
                with st.spinner("Generating summary..."):
                    display_summary_results(input_text, summarization_type, abs_settings, ext_settings)
            else:
                st.error("Please enter valid text to summarize.")
    
    # Display method information
    display_method_info()

if __name__ == "__main__":
    main()