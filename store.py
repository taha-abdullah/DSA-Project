import sqlite3


def findey(*args):
    conn = sqlite3.connect("forward.db")
    result = []
    heading = []
    # cursor to move around the database
    c = conn.cursor()
    for i in args:
        head = c.execute("SELECT heading FROM forward WHERE heading = ?", (i,))
        head = c.fetchall()
        heading.append(head)
        res = c.execute("SELECT doc_id FROM words WHERE word = ?", (i,))
        res = c.fetchall()
        result.append(res)

    return result, heading


def rank(result, heading):
    print(result)
    print(head)
    if heading
    urls = []

    return


de, gh = findey('fairchild', 'orphan')
rank(de, gh)