from flask import Flask, request, render_template, send_from_directory
import os
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = Flask(__name__)

index_dir = "index"

def search_index(query_str):
    ix = open_dir(index_dir)
    parser = QueryParser("content", ix.schema)
    query = parser.parse(query_str)

    results = []
    with ix.searcher() as searcher:
        hits = searcher.search(query, limit=None)
        for hit in hits:
            results.append(hit['path'])
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = search_index(query)
    return render_template('results.html', query=query, results=results)

@app.route('/pdf/<path:filename>')
def pdf_view(filename):
    directory = os.path.dirname(filename)
    filename = os.path.basename(filename)
    return send_from_directory(directory, filename)

if __name__ == "__main__":
    app.run(debug=True)

