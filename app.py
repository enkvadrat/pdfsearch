from flask import Flask, request, render_template, send_from_directory

import os
from datetime import datetime, timedelta
import time
from threading import Thread

app = Flask(__name__)

import config

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    import search
    query = request.form['query']
    results = search.sqlite_search(query)
    return render_template('results.html', query=query, results=results)

@app.route('/pdf/<path:filename>')
def pdf_view(filename):
    directory = os.path.dirname(filename)
    filename = os.path.basename(filename)
    return send_from_directory(directory, filename)

def import_new_pdf(hours:int=1):
    import extract
    import sharepoint

    while True:
        # download new pdf
        sharepoint.main()
        extract.process_pdfs(config.certificate_folder,config.certificate_db_file)

        now = datetime.now()
        next_run = now + timedelta(hours=hours)

        time_to_sleep = (next_run - now).total_seconds()
        time.sleep(time_to_sleep)


if __name__ == "__main__":

    task_thread = Thread(target=import_new_pdf)
    task_thread.daemon = True
    task_thread.start()
   
    app.run(debug=False,port=4000)

