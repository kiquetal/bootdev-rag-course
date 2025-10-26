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
- ✅ Implemented inverted index for efficient search
- ✅ Added support for limiting search results to top 5 matches
- ✅ Enhanced search to work with multi-word queries

### Inverted Index Implementation
- Built an inverted index data structure for faster searching
- Index maps tokens to document IDs containing those tokens
- Maintains a document map for quick lookup of movie details
- Implements term frequency tracking using Python's Counter collection
- Supports saving and loading index state using pickle
- Applies consistent text processing (stemming, punctuation removal) during indexing and searching

#### Term Frequency Implementation
The inverted index now includes term frequency tracking using Python's Counter collection:

1. **What is Term Frequency?**
   - Counts how many times each token appears in a document
   - Stored per document using Python's Counter class
   - Uses stemmed tokens for consistent counting

2. **Counter Implementation Details:**
   - Each document has its own Counter object
   - Tokens are stemmed before counting
   - Stopwords are removed before counting
   - Frequencies are stored with stemmed terms as keys

3. **Benefits of Using Counter:**
   - Efficient counting of term occurrences
   - Easy access to term frequencies
   - Built-in methods for most common terms
   - Automatic handling of new terms

4. **How it's used in the code:**
   - During indexing: Creates Counter per document
   - During search: Access term frequencies for ranking
   - For term frequency queries: Quick lookups of specific terms

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

### Building the Index
Before searching, you need to build the inverted index:
```bash
python -m hoopla.cli.keyword_search_cli build
```
This will create the index and save it to the cache directory.

### Searching
To search using the inverted index:
```bash
python -m hoopla.cli.keyword_search_cli search "<your query>"
```

Example searches:
```bash
# Search for a single word
python -m hoopla.cli.keyword_search_cli search "brave"

# Search for multiple words
python -m hoopla.cli.keyword_search_cli search "brave man"

# Search ignoring punctuation
python -m hoopla.cli.keyword_search_cli search "assault!"
```

The search will:
- Remove punctuation from your query
- Apply stemming to match word variations
- Return up to 5 most relevant results
- Show movie IDs and titles for matches

### Term Frequency Lookup
To check how many times a term appears in a specific document:
```bash
python -m hoopla.cli.keyword_search_cli tf <doc_id> "<term>"
```

Example:
```bash
# Check frequency of "brave" in document 1
python -m hoopla.cli.keyword_search_cli tf 1 "brave"

# Note: Terms are stemmed before lookup, so different forms of a word will match
# For example, "running" will match with "run"
python -m hoopla.cli.keyword_search_cli tf 1 "running"
```

Note: The term frequency command:
- Stems the input term (e.g., "running" becomes "run")
- Removes punctuation and converts to lowercase
- Returns the frequency of the stemmed term in the specified document
- Only works with single tokens (not phrases)

### Saving and Loading an Inverted Index (pickle)
The project now includes a minimal InvertedIndex class and support for saving the index to disk using Python's built-in pickle module.

Example:
```
from hoopla.cli.keyword_search_cli import InvertedIndex, load_data

# Build the index from the bundled movies dataset
records = load_data("movies.json")

idx = InvertedIndex()
# Populate the document map (expects dict[int, dict])
for rec in records:
    doc_id = int(rec.get("id", 0))
    idx.docmap[doc_id] = rec

# Build postings and save to disk
idx.build()
idx.save("index.pkl")
```

Note: pickle is part of Python's standard library, so you don't need to install anything extra to use it.

## Next Steps
- Add vector embeddings for semantic search
- Implement TF-IDF scoring for better relevance ranking
- Create a full RAG pipeline with LLM integration
