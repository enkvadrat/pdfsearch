from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
import json

def create_search_index(index_dir, json_file):
    schema = Schema(path=ID(stored=True, unique=True), content=TEXT)
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    ix = index.create_in(index_dir, schema)

    writer = ix.writer()
    with open(json_file, 'r') as f:
        pdf_texts = json.load(f)
        for path, content in pdf_texts.items():
            writer.add_document(path=path, content=content)
    writer.commit()

def search_index(index_dir, query_str):
    ix = index.open_dir(index_dir)
    parser = QueryParser("content", ix.schema)
    query = parser.parse(query_str)

    results = []
    with ix.searcher() as searcher:
        hits = searcher.search(query, limit=None)
        for hit in hits:
            results.append(hit['path'])
    
    return results

if __name__ == "__main__":
    index_dir = "index"
    json_file = "certificate_texts.json"
    # need chaning so it only gets created if json_file changes
    create_search_index(index_dir, json_file)
    
    # Example search
    query_str = "Test"
    results = search_index(index_dir, query_str)
    print(f"Found in files: {results}")
