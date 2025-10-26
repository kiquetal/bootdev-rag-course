from collections import Counter

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
