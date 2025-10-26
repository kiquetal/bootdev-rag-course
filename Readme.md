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
