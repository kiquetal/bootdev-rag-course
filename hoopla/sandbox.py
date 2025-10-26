from collections import Counter
from typing import Dict, Any, Set

class InvertedIndexExample:
    def __init__(self):
        # Main inverted index: token -> set of doc_ids
        self.index: Dict[str, Set[int]] = {}
        # Store document metadata
        self.docmap: Dict[int, Dict[str, Any]] = {}
        # Store term frequencies per document: doc_id -> Counter of terms
        self.term_frequencies: Dict[int, Counter] = {}

    def add_document(self, doc_id: int, text: str) -> None:
        """
        Demonstrates how to count token frequencies for a specific document

        Args:
            doc_id: The ID of the document
            text: The text content of the document
        """
        # Convert to lowercase and split into tokens
        tokens = text.lower().split()

        # Create a new Counter for this specific document ID
        # This will automatically count all occurrences of each token
        self.term_frequencies[doc_id] = Counter(tokens)

        # Add to inverted index
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

# Example usage:
print("\nDemonstrating add_document with Counter:")
print("-" * 50)

index = InvertedIndexExample()

# Add some sample documents
documents = {
    1: "the brave cat and the brave dog",
    2: "the quick cat was brave",
}

for doc_id, text in documents.items():
    index.add_document(doc_id, text)
    print(f"\nDocument {doc_id} added:")
    print(f"Text: {text}")
    print(f"Term frequencies for this document:")
    print(dict(index.term_frequencies[doc_id]))

print("\nFinal term frequencies per document:")
for doc_id, frequencies in index.term_frequencies.items():
    print(f"\nDocument {doc_id}:")
    print(f"- Most common terms: {frequencies.most_common(2)}")
    print(f"- Count of 'brave': {frequencies['brave']}")
    print(f"- Count of 'the': {frequencies['the']}")

print("\nInverted index contents:")
print(dict(index.index))

# Example 1: Basic Counter usage with a list
fruits = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
fruit_counter = Counter(fruits)
print("Basic Counter with fruits:")
print(fruit_counter)  # Counter({'apple': 3, 'banana': 2, 'orange': 1})
print(f"Count of apples: {fruit_counter['apple']}")
print(f"Most common fruit: {fruit_counter.most_common(1)}")

# Example 2: Using Counter for document token counting
documents = {
    1: "the brave man went to battle",
    2: "the battle was fierce and brave",
    3: "a man needs courage to be brave"
}

# Store frequency per document
doc_frequencies = {}

for doc_id, text in documents.items():
    # Split text into tokens and create Counter
    tokens = text.lower().split()
    doc_frequencies[doc_id] = Counter(tokens)

print("\nDocument token frequencies:")
for doc_id, counter in doc_frequencies.items():
    print(f"\nDocument {doc_id}:")
    print(f"Token counts: {dict(counter)}")
    print(f"Most common tokens: {counter.most_common(2)}")
    print(f"Count of 'brave' in doc: {counter['brave']}")

# Example 3: Combining Counters
print("\nCombining counters from multiple documents:")
total_frequencies = Counter()
for counter in doc_frequencies.values():
    total_frequencies.update(counter)

print(f"Total token frequencies across all docs: {dict(total_frequencies)}")
print(f"Most common tokens overall: {total_frequencies.most_common(3)}")

# Example 4: Counter operations
doc1_counter = doc_frequencies[1]
doc2_counter = doc_frequencies[2]

print("\nCounter operations:")
print(f"Tokens in doc1: {dict(doc1_counter)}")
print(f"Tokens in doc2: {dict(doc2_counter)}")
print(f"Sum of frequencies: {dict(doc1_counter + doc2_counter)}")
print(f"Tokens common to both docs: {dict(doc1_counter & doc2_counter)}")

print("\nExample: Understanding Document ID and Token Counting")
print("-" * 50)

# Each document has an ID and some text
documents = {
    101: "the cat and the dog",
    102: "the cat was quick",
    103: "dog and dog run"
}

# We'll store token frequencies for each document ID
doc_frequencies = {}

# Process each document
for doc_id, text in documents.items():
    tokens = text.lower().split()
    # Create a Counter for this specific document
    doc_frequencies[doc_id] = Counter(tokens)

    print(f"\nDocument ID: {doc_id}")
    print(f"Text: {text}")
    print(f"Token frequencies in this document:")
    print(f"  {dict(doc_frequencies[doc_id])}")

print("\nAccessing specific token counts:")
# For document 101, how many times does "the" appear?
print(f"'the' appears {doc_frequencies[101]['the']} times in document 101")
# For document 103, how many times does "dog" appear?
print(f"'dog' appears {doc_frequencies[103]['dog']} times in document 103")

print("\nMost common tokens per document:")
for doc_id in documents:
    print(f"Document {doc_id}: {doc_frequencies[doc_id].most_common(2)}")
