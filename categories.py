import sqlite3

conn = sqlite3.connect('./knowledge.db')
c = conn.cursor()

def cat_analysis():
    print "Calculating category totals"
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories AS
            SELECT category as category
                , sum(total) as total
                FROM books
                GROUP BY category''')

    print "Calculating category tfs"
    c.execute('''
        CREATE TABLE IF NOT EXISTS cat_words AS
            SELECT categories.category AS category
                , word AS word
                , cast(sum(freq) as real)/categories.total AS tf
            FROM book_words, books, categories
            WHERE book_words.file = books.file 
                AND categories.category = books.category
            GROUP BY categories.category, word
        ''')

def relevance():
    print "Calculating category tf * idfs"
    c.execute('''
        CREATE TABLE IF NOT EXISTS relevant AS
        SELECT category AS category
            , words.word AS word
            , tf * idf AS relevance
        FROM cat_words, words
        WHERE words.word = cat_words.word 
        ''')

#cat_analysis()
relevance()
conn.commit()
