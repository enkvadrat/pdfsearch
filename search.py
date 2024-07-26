import sqlite3

def sqlite_search(query_str):
    import config
    db_path = config.certificate_db_file
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT path FROM pdfs WHERE text MATCH ?', (query_str,))
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results

if __name__ == "__main__":
    q = input("Search: ")
    print(sqlite_search(q))

    
