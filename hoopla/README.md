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

## Understanding Tokenization

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

## Project Structure
```
hoopla/
├── data/           # JSON data files
├── cli/            # Command-line interface tools
│   └── keyword_search_cli.py  # Simple tokenized search implementation
└── README.md       # This documentation
```

## Usage
To use the search functionality:
```
python -m hoopla.cli.keyword_search_cli search <query>
```

This will search through the data using tokenization and return the most relevant results.

## Next Steps
- Implement more advanced text processing (stemming, lemmatization)
- Add vector embeddings for semantic search
- Create a full RAG pipeline with LLM integration

