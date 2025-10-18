#!/usr/bin/env python3

import argparse
import json
import string
from pathlib import Path
from typing import Any, Dict, List
from nltk.stem import PorterStemmer

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
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()

