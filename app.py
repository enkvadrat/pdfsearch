from flask import Flask, request, render_template, send_from_directory

import os
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from datetime import datetime, timedelta
import time
from threading import Thread

app = Flask(__name__)

import config


def search_index(query_str):
    results = []
    try:
        ix = open_dir(config.index)
    except Exception as e:
       print(f"Failed to open index when someone tried to search for a pdf: {e}")
       return results

    parser = QueryParser("content", ix.schema)
    query = parser.parse(query_str)

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

def update_pdf(hours:int=1):
    import extract
    import index

    while True:

        # download pdfs
        import sharepoint

        extract.process_pdfs(config.certificate_folder,config.certificate_json_file)

        index.create_search_index(config.index, config.certificate_json_file)

        now = datetime.now()
        next_run = now + timedelta(hours=hours)

        time_to_sleep = (next_run - now).total_seconds()
        time.sleep(time_to_sleep)


if __name__ == "__main__":

    task_thread = Thread(target=update_pdf)
    task_thread.daemon = True
    task_thread.start()
   
    app.run(debug=True,port=4000)

