import sqlite3
import re

def escape_special_chars(query_str):
    # Define characters that must be quoted in FTS5
    special_chars = re.compile(r'([^\w\s\u0080-\uFFFF])')
    # escape the whole string with double qoutes if it contains special chars
    if special_chars.search(query_str):
        query_str = f'"{query_str}"'
    return query_str

def sqlite_search(query_str):
    results = []
    import config
    db_path = config.certificate_db_file
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query_str = escape_special_chars(query_str)
    print(f"Searched: {query_str}")
    try:
        c.execute('''SELECT path FROM pdfs WHERE text MATCH ?
        ''', (query_str,))
        results = [row[0] for row in c.fetchall()]
    except Exception as e:
        print(f"{e}")
    conn.close()
    return results


if __name__ == "__main__":
    q = input("Search: ")
    res = sqlite_search(q)
    count = 0
    for r in res:
        count += 1
    print(f"Matches: {count}")
    
