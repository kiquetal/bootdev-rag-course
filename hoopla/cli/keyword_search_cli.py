#!/usr/bin/env python3

import argparse
import json
import string
import pickle
from pathlib import Path
from typing import Any, Dict, List
from nltk.stem import PorterStemmer



class InvertedIndex:
    """
    Minimal inverted index container.

    Attributes:
        index: Mapping from term -> set of document ids containing the term.
        docmap: Mapping from document id -> original document payload.
    """

    def __init__(self) -> None:
        self.index: Dict[str, set[int]] = {}
        self.docmap: Dict[int, Dict[str, Any]] = {}

    def save(self) -> None:
        """
        Save the index using the pattern cache/index.pkl
        Save the docmap using the pattern cache/docmap.pkl


        """
        # check if cache directory exists
        base = Path(__file__).resolve().parents[1]  # .../hoop
        cache_path = base / "cache"
        if not cache_path.exists():
            cache_path.mkdir(parents=True, exist_ok=True)
        index_path = cache_path / "index.pkl"
        docmap_path = cache_path / "docmap.pkl"
        with index_path.open("wb") as fh:
            pickle.dump(self.index, fh)
        with docmap_path.open("wb") as fh:
            pickle.dump(self.docmap, fh)


    def __add_document(self, doc_id: int, text: str) -> None:
        """
        Add a document to the inverted index.
        First tokenize then add each token to the index.
        """
        text_lower = text.lower()
        tokens = text_lower.split()

        # should remove punctuation from tokens

        table = str.maketrans('', '', string.punctuation)
        tokens = [token.translate(table) for token in tokens]
        # replace the ` with '
        tokens = [token.replace('`', "'") for token in tokens]

        tokens = [token for token in tokens if token]  # REMOVE empty tokens
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            # add the doc_id to the set for the index
            self.index[token].add(doc_id)


    def get_documents(self, term: str) -> List[int]:
        """
        Get list of document ids containing the term.
        Apply the same normalization/tokenization as __add_document and
        return the union of postings for all tokens in the term.
        """
        if not term:
            return []

        # follow the same transform steps used in __add_document
        term_lower = term.lower()
        tokens = term_lower.split()

        table = str.maketrans('', '', string.punctuation)
        tokens = [token.translate(table) for token in tokens]
        tokens = [token.replace('`', "'") for token in tokens]
        tokens = [token for token in tokens if token]  # remove empty tokens

        postings: set[int] = set()
        for token in tokens:
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
def main() -> None:
    parser = argparse.ArgumentParser(description="Simple Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies by keyword")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--data-file", type=str, default="movies.json",
                              help="JSON filename located in hoopla/data (default: movies.json)")
    build_parser = subparsers.add_parser("build", help="Build the inverted index and save to cache")


    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            try:
                records = load_data(args.data_file)
                results = search_records(records, args.query)
                print(f"Found {len(results)} matching records")
                for idx, record in enumerate(results[:5], 1):
                    print(f"{idx}. {record.get('title')}")
            except FileNotFoundError:
                print(f"Data file not found: hoopla/data/{args.data_file}")
        case "build":
            print("Building inverted index...")
            index = InvertedIndex()
            index.build()
            index.save()
            docs = index.get_documents("merida")
            print(f"First document for token 'merida': {docs[0] if docs else 'No documents found'}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
