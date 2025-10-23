### Course Learn Retrieval Augmented Generation

This repository contains the Hoopla project used throughout the Boot.dev RAG course. It includes a simple keyword search CLI and a minimal inverted index.

Quick start:
- Run a search: `python -m hoopla.cli.keyword_search_cli search "your query"`
- Save an index with pickle (stdlib): see hoopla/README.md for a short example.

## Features

### Text Processing
- Tokenization for improved search relevance
- Stopwords filtering to improve search quality
- Stemming using NLTK's PorterStemmer
- Enhanced partial token matching

### Inverted Index
- Minimal InvertedIndex class for efficient search
- Support for saving and loading index to disk using Python's pickle module
- Document mapping for fast document retrieval

