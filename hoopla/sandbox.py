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
