# Hoopla - Bootdev RAG Course

## Project Overview
This project is part of the Bootdev Retrieval-Augmented Generation (RAG) course. The goal is to implement increasingly sophisticated search and retrieval techniques for enhancing large language model interactions.

## Current Progress

### Basic Search Implementation
- ✅ Created a simple CLI search tool that reads JSON data
- ✅ Implemented basic keyword matching functionality
- ✅ Added sorting capabilities for search results (by relevance and ID)

### Tokenization-Based Search
- ✅ Implemented basic tokenization for improved search relevance
- ✅ Search algorithm now matches on individual tokens instead of exact string matches
- ✅ Added stopwords filtering to improve search quality
- ✅ Implemented punctuation removal for better token matching

### Advanced Text Processing
- ✅ Implemented stemming using NLTK's PorterStemmer
- ✅ Enhanced partial token matching to find query terms within document terms
- ✅ Improved sanitization of text by removing punctuation

## Understanding Tokenization and Text Processing

Tokenization is a fundamental technique in information retrieval and natural language processing that involves breaking text into smaller units called tokens. In our implementation:

1. **What is tokenization?**
   - Text is split into individual words or tokens
   - Common processing includes lowercasing, removing punctuation, and filtering stop words

2. **Why tokenization matters for search:**
   - Enables more flexible matching beyond exact string comparison
   - Allows for relevance scoring based on token frequency
   - Improves search quality by matching partial terms

3. **Our tokenization approach:**
   - Simple whitespace/punctuation-based tokenization
   - Case-insensitive matching
   - Relevance scoring based on token match frequency
   - Stopwords removal using a dedicated stopwords list
   - Partial token matching (finding query tokens within title tokens)

4. **Stemming implementation:**
   - Uses Porter Stemming algorithm via NLTK
   - Reduces words to their root form (e.g., "running" → "run")
   - Allows matching different forms of the same word
   - Applied to both query tokens and document tokens for consistent matching

## Project Structure
```
hoopla/
├── data/           # JSON data files
│   └── stopwords.txt  # List of common words to filter out
├── cli/            # Command-line interface tools
│   └── keyword_search_cli.py  # Tokenized search with stemming implementation
└── README.md       # This documentation
```

## Usage
To use the search functionality:
```
python -m hoopla.cli.keyword_search_cli search <query>
```

This will search through the data using tokenization, stemming, and return the most relevant results.

## Next Steps
- Add vector embeddings for semantic search
- Implement TF-IDF scoring for better relevance ranking
- Create a full RAG pipeline with LLM integration
