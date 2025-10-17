#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

def load_data(filename: str = "data.json") -> List[Dict[str, Any]]:
    """
    Load JSON from hoopla/data/<filename> and return a list of records
    sorted by 'id' in descending order.
    Handles either:
      - a dict mapping id -> record
      - a dict of records where each value has an 'id' field
      - a list of records where each record has an 'id' field
    """
    base = Path(__file__).resolve().parents[1]  # .../hoopla
    data_path = base / "data" / filename
    try:
        with data_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        raise
    # If it's a dict keyed by id (string or int)
    if isinstance(data, dict):
        # try sorting by numeric keys first
        try:
            sorted_items = sorted(data.items(), key=lambda kv: int(kv[0]), reverse=True)
            return [v for _, v in sorted_items]
        except Exception:
            # fallback: sort by 'id' inside values
            try:
                return sorted(list(data.values()), key=lambda v: int(v.get("id", 0)), reverse=True)
            except Exception:
                return list(data.values())
    # If it's a list of records
    if isinstance(data, list):
        try:
            return sorted(data, key=lambda v: int(v.get("id", 0)), reverse=True)
        except Exception:
            return data
    return []

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search Cli")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser =  subparsers.add_parser("search",help="Search movies using BM25")
    search_parser.add_argument("query",type=str,help="Search query")
    search_parser.add_argument("--data-file", type=str, default="data.json",
                               help="JSON filename located in hoopla/data (default: data.json)")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            try:
                records = load_data(args.data_file)
            except FileNotFoundError:
                print(f"Data file not found: hoopla/data/{args.data_file}")
                return
            # brief summary: count and top 5 ids (if present)
            print(f"Loaded {len(records)} records (sorted by id desc).")
            for rec in records[:5]:
                rid = rec.get("id") if isinstance(rec, dict) else None
                print(f" - id={rid}  {rec}")
        case _:
            parser.print_help()

if __name__== "__main__":
    main()
