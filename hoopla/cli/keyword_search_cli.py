#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

def load_data(filename: str = "movies.json") -> List[Dict[str, Any]]:
    """Load JSON from data directory and sort by id in descending order"""
    base = Path(__file__).resolve().parents[1]  # .../hoopla
    data_path = base / "data" / filename

    with data_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    # Convert to list if it's a dictionary
    if isinstance(data, dict):
        data = list(data.values())

    # Sort by id in descending order
    try:
        return sorted(data, key=lambda x: int(x.get("id", 0)), reverse=True)
    except:
        return data

def search_records(records: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Simple search function that looks for query in title or description.
    Returns matches sorted by id in descending order.
    """
    query = query.lower()
    results = []

    for record in records:
        title = record.get("title", "").lower()
        description = record.get("description", "").lower()

        if query in title or query in description:
            results.append(record)

    return results

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
                for record in results[:10]:
                    print(f" - id={record.get('id')} title={record.get('title')}")
            except FileNotFoundError:
                print(f"Data file not found: hoopla/data/{args.data_file}")
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
