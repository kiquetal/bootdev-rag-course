#!/usr/bin/env python3

import argparse
import json
import string
import pickle
from pathlib import Path
from typing import Any, Dict, List, Counter
from nltk.stem import PorterStemmer



class InvertedIndex:
    """
    Minimal inverted index container.

    Attributes:
        index: Mapping from term -> set of document ids containing the term.
        docmap: Mapping from document id -> original document payload.
        term_frequency: Mapping from term -> frequency count across all documents.
    """

    def __init__(self) -> None:
        self.index: Dict[str, set[int]] = {}
        self.docmap: Dict[int, Dict[str, Any]] = {}
        self.term_frequency: Dict[int, Counter[str]] = {}

    def load(self):
        """
        Load the index from the pattern cache/index.pkl
        Load the docmap from the pattern cache/docmap.pkl
        Load term_frequency from cache/term_frequency.pkl
        """
        base = Path(__file__).resolve().parents[1]  # .../hoop
        cache_path = base / "cache"
        index_path = cache_path / "index.pkl"
        docmap_path = cache_path / "docmap.pkl"
        termfreq_path = cache_path / "term_frequency.pkl"

        # Raise error if files do not exist
        if not index_path.exists() or not docmap_path.exists() or not termfreq_path.exists():
            raise FileNotFoundError("Index or docmap or termfreq file not found in cache directory.")

        with index_path.open("rb") as fh:
            self.index = pickle.load(fh)
        with docmap_path.open("rb") as fh:
            self.docmap = pickle.load(fh)
        with termfreq_path.open("rb") as fh:
            self.term_frequency = pickle.load(fh)


    def save(self) -> None:
        """
        Save the index using the pattern cache/index.pkl
        Save the docmap using the pattern cache/docmap.pkl
        Save term_frequency using the pattern cache/term_frequency.pkl

        """
        # check if cache directory exists
        base = Path(__file__).resolve().parents[1]  # .../hoop
        cache_path = base / "cache"
        if not cache_path.exists():
            cache_path.mkdir(parents=True, exist_ok=True)
        index_path = cache_path / "index.pkl"
        docmap_path = cache_path / "docmap.pkl"
        termfreq_path = cache_path / "term_frequency.pkl"
        with index_path.open("wb") as fh:
            pickle.dump(self.index, fh)
        with docmap_path.open("wb") as fh:
            pickle.dump(self.docmap, fh)
        with termfreq_path.open("wb") as fh:
            pickle.dump(self.term_frequency, fh)

    def __add_document(self, doc_id: int, text: str) -> None:
        """
        Add a document to the inverted index.
        First tokenize, clean, stem, then add each token to the index.
        """
        # Initialize stemmer
        stemmer = PorterStemmer()

        text_lower = text.lower()
        tokens = text_lower.split()

        # Remove punctuation from tokens
        table = str.maketrans('', '', string.punctuation)
        tokens = [token.translate(table) for token in tokens]
        tokens = [token.replace('`', "'") for token in tokens]
        tokens = [token for token in tokens if token]  # Remove empty tokens

        # Remove stopwords
        base = Path(__file__).resolve().parents[1]
        stopwords_path = base / "data" / "stopwords.txt"
        with stopwords_path.open("r", encoding="utf-8") as fh:
            stopwords = set(line.strip() for line in fh)

        # Filter stopwords and stem the tokens
        filtered_tokens = [token for token in tokens if token not in stopwords]
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

        # Create Counter with stemmed tokens
        token_counts = Counter(stemmed_tokens)
        self.term_frequency[doc_id] = token_counts

        # Add stemmed tokens to inverted index
        for token in stemmed_tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)


    def get_documents(self, term: str) -> List[int]:
        """
        Get list of document ids containing the term.
        Apply the same normalization/tokenization as __add_document and
        return the union of postings for all tokens in the term.
        """
        if not term:
            return []

        # Initialize stemmer
        stemmer = PorterStemmer()

        # Follow the same transform steps used in __add_document
        term_lower = term.lower()
        tokens = term_lower.split()

        # Clean tokens
        table = str.maketrans('', '', string.punctuation)
        tokens = [token.translate(table) for token in tokens]
        tokens = [token.replace('`', "'") for token in tokens]
        tokens = [token for token in tokens if token]  # remove empty tokens

        # Remove stopwords
        base = Path(__file__).resolve().parents[1]
        stopwords_path = base / "data" / "stopwords.txt"
        with stopwords_path.open("r", encoding="utf-8") as fh:
            stopwords = set(line.strip() for line in fh)

        # Filter stopwords and stem the tokens
        filtered_tokens = [token for token in tokens if token not in stopwords]
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

        # Get postings for stemmed tokens
        postings: set[int] = set()
        for token in stemmed_tokens:
            postings |= self.index.get(token, set())

        return sorted(postings)

    def build(self)-> None:
        """
        Build the inverted index from the docmap.
        """
        data = self.__load_data()
        for record in data:
            doc_id = int(record.get("id", 0))
            title = record.get("title", "")
            description = record.get("description", "")
            full_text = f"{title} {description}"
            self.docmap[doc_id] = record
            self.__add_document(doc_id, full_text)


    def __load_data(self, filename: str = "movies.json") -> List[Dict[str, Any]]:
        """Load JSON from data directory and sort by id in descending order"""

        base = Path(__file__).resolve().parents[1]  # .../hoopla
        data_path = base / "data" / filename


        with data_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)

        # Extract the movies list from the dictionary
        if isinstance(data, dict) and "movies" in data:
            data = data["movies"]

        try:
            return sorted(data, key=lambda x: int(x.get("id", 0)), reverse=False)
        except:
            return data

    def get_tf(self, doc_id: int, term: str) -> int:
        """
        Get the term frequency of a term in a specific document.
        The term will be stemmed before lookup since we store stemmed terms.
        """
        if ' ' in term:
            raise ValueError("Term frequency can only be retrieved for single tokens.")

        # Initialize stemmer and process the term
        stemmer = PorterStemmer()
        term_lower = term.lower()

        # Clean the term
        table = str.maketrans('', '', string.punctuation)
        cleaned_term = term_lower.translate(table)
        cleaned_term = cleaned_term.replace('`', "'")

        if not cleaned_term:
            return 0

        # Stem the term
        stemmed_term = stemmer.stem(cleaned_term)

        # Look up frequency of stemmed term
        return self.term_frequency[doc_id].get(stemmed_term, 0)

def isPartialMatch(record: str, query: str) -> bool:
    """
    Check if the query is a partial match in the title or description of the record.
    """

    tokensTitle = record.split()
    tokensQuery = query.split()

    # read file stopwords.txt
    base = Path(__file__).resolve().parents[1]  # .../hoop
    stopwords_path = base / "data" / "stopwords.txt"
    with stopwords_path.open("r", encoding="utf-8") as fh:
        stopwords = set(line.strip() for line in fh)

    # REMOVE empty tokens
    tokensTitle = [token for token in tokensTitle if token]
    tokensTitle = [token for token in tokensTitle if token not in stopwords]
    tokensQuery = [token for token in tokensQuery if token]
    tokensQuery = [token for token in tokensQuery if token not in stopwords]

    # STEMMING
    ps = PorterStemmer()
    tokensTitle = [ps.stem(token) for token in tokensTitle]
    tokensQuery = [ps.stem(token) for token in tokensQuery]

    for qtoken in tokensQuery:
        for ttoken in tokensTitle:
            if qtoken in ttoken:
                return True


    return False


def load_data(filename: str = "movies.json") -> List[Dict[str, Any]]:
    """Load JSON from data directory and sort by id in descending order"""
    base = Path(__file__).resolve().parents[1]  # .../hoopla
    data_path = base / "data" / filename


    with data_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    # Extract the movies list from the dictionary
    if isinstance(data, dict) and "movies" in data:
        data = data["movies"]

    try:
        return sorted(data, key=lambda x: int(x.get("id", 0)), reverse=False)
    except:
        return data

def search_records(records: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Simple search function that looks for query in title or description.
    Returns matches sorted by id in descending order.
    """
    query = query.lower()
    santitizedQuery = query.translate(str.maketrans('', '', string.punctuation))
    results = []

    for record in records:
        # Skip if record is not a dictionary
        if not isinstance(record, dict):
            continue

        title = record.get("title", "").lower()
        sanitized_title = title.translate(str.maketrans('', '', string.punctuation))

        if isPartialMatch(sanitized_title, santitizedQuery):
            results.append(record)

    return sorted(results, key=lambda x: int(x.get("id", 0)))
def get_tf(inverted_index: InvertedIndex, doc_id: int, term: str) -> int:
    """
    Get the term frequency of a term in a specific document using the inverted index.
    """
    if doc_id not in inverted_index.docmap:
        raise ValueError(f"Document ID {doc_id} not found in docmap.")

    # Clean the term
    table = str.maketrans('', '', string.punctuation)
    cleaned_term = term.lower().translate(table)
    ## Use the PorterStemmer to stem the term
    stemmer = PorterStemmer()
    stemmed_term = stemmer.stem(cleaned_term)
    ## Get the frequency from the inverted index
    frequency = inverted_index.get_tf(doc_id, stemmed_term)
    return frequency
def main() -> None:
    parser = argparse.ArgumentParser(description="Simple Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies by keyword")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--data-file", type=str, default="movies.json",
                              help="JSON filename located in hoopla/data (default: movies.json)")
    build_parser = subparsers.add_parser("build", help="Build the inverted index and save to cache")
    build_parser.add_argument("--data-file", type=str, default="movies.json",
                              help="JSON filename located in hoopla/data (default: movies.json)")

    tf_parser = subparsers.add_parser("tf", help="Get term frequency for a term in a document")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term to get frequency for")



    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            try:
                inverted_index = InvertedIndex()
                inverted_index.load()
                # Clean query: remove punctuation and convert to lowercase
                query = args.query.translate(str.maketrans('', '', string.punctuation)).lower()
                results = set()
                stemmer = PorterStemmer()
                # Stem the search token
                search_stems = [stemmer.stem(token) for token in query.split()]

                for doc_id in inverted_index.docmap:
                    record = inverted_index.docmap[doc_id]
                    # Clean and stem the words in the document
                    description = record.get('description', '').translate(str.maketrans('', '', string.punctuation)).lower()
                    title = record.get('title', '').translate(str.maketrans('', '', string.punctuation)).lower()
                    doc_words = description.split() + title.split()
                    doc_stems = [stemmer.stem(word) for word in doc_words]

                    # Check if any search stem matches document stems
                    if any(stem in doc_stems for stem in search_stems):
                        results.add(doc_id)

                    if len(results) >= 5:
                        results = set(sorted(list(results))[:5])
                        break

                for doc_id in sorted(results):
                    record = inverted_index.docmap.get(doc_id, {})
                    print(f"ID: {record.get('id', '')}, Title: {record.get('title', '')}")

            except FileNotFoundError:
                print(f"Data file not found: hoopla/data/{args.data_file}")
        case "build":

            print("Building inverted index...")
            index = InvertedIndex()
            index.build()
            index.save()
            print(f"Inverted index built and saved to cache.")

        case "tf":
            try:
                inverted_index = InvertedIndex()
                inverted_index.load()
                frequency = get_tf(inverted_index, args.doc_id, args.term)
                print(f"Term frequency of '{args.term}' in document {args.doc_id}: {frequency}")
            except ValueError as e:
                print(e)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
