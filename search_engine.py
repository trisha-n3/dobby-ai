# search_engine.py
from semantic_search import semantic_search

def search_documents(query, documents):
    results = semantic_search(query, documents)
    return results  # make sure each result has "text" and "source" keys