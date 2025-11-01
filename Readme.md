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

### TF-IDF Implementation
- Term Frequency (TF): Measures how frequently a term appears in a document
  - Implemented using Counter collection for efficient token counting
  - Normalizes text by removing punctuation and applying stemming
  - Excludes stopwords for better relevance

- Inverse Document Frequency (IDF): Measures how important a term is across all documents
  - Calculated using the formula: log((N + 1) / (df + 1))
  - N is the total number of documents
  - df is the document frequency (number of documents containing the term)
  - The +1 in formula provides smoothing to handle edge cases

- TF-IDF Score: Combines TF and IDF to rank document relevance
  - Higher scores indicate terms that are both frequent in a document and rare across all documents
  - Used to identify distinctive terms in documents

### Command Line Interface
- Search documents: `uv run cli/keyword_search_cli.py search "query"`
- Calculate term frequency: `uv run cli/keyword_search_cli.py tf doc_id term`
- Get IDF score: `uv run cli/keyword_search_cli.py idf term`
- Calculate TF-IDF: `uv run cli/keyword_search_cli.py tfidf doc_id term`

### Inverted Index
- Minimal InvertedIndex class for efficient search
- Support for saving and loading index to disk using Python's pickle module
- Document mapping for fast document retrieval

## Project Setup

### Setting up with uv (Recommended)

uv is a fast Python package installer and virtual environment manager. Here's how to get started:

1. **Install uv:**
```bash
pip install uv
```

2. **Create and activate a virtual environment:**
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# OR
.venv\Scripts\activate  # On Windows
```

3. **Install dependencies:**
```bash
uv pip install -r requirements.txt
```

4. **Add new dependencies:**
```bash
uv pip install package_name
uv pip freeze > requirements.txt
```

### Project Standards

1. **Dependencies Management:**
   - Use `requirements.txt` for package dependencies
   - Use `uv.lock` for dependency locking (automatically managed by uv)
   - Always update requirements.txt after adding new packages

2. **Virtual Environment:**
   - Never commit .venv directory
   - Always use virtual environment when developing
   - One virtual environment per project

3. **Package Structure:**
   - Keep code in the `hoopla/` directory
   - Tests in `tests/` directory
   - Configuration in project root

4. **Code Style:**
   - Follow PEP 8 guidelines
   - Use type hints
   - Document functions and classes
   - Keep functions focused and small
