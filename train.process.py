import sqlite3

conn = sqlite3.connect('./knowledge.db')
c = conn.cursor()

def cat_analysis():
    print "Calculating category totals"
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories AS
            SELECT category AS category
                , count(*) AS books
                , sum(total) AS words
            FROM books
            GROUP BY category
        ''')

    print "Calculating category tfs"
    c.execute('''
        CREATE TABLE IF NOT EXISTS cat_words AS
            SELECT category AS category
                , word AS word
                , cast(sum(freq) AS real) / words AS tf
            FROM book_words NATURAL JOIN books NATURAL JOIN categories
            GROUP BY category, word;
        ''')

def relevance():
    print "Calculating category tf * idfs"
    c.execute('''
        CREATE TABLE IF NOT EXISTS relevant AS
            SELECT category AS category
                , word AS word
                , tf * idf AS relevance
            FROM cat_words, words USING (word)
        ''')

def indicators():
    print "Selecting top 1000 indicative words"
    c.execute('''
        CREATE TABLE IF NOT EXISTS indicators AS
            SELECT category AS category
                , word as word
                , relevance as score
            FROM relevant
            ORDER BY relevance DESC
            LIMIT 1000
        ''')

def training_table():
    print "Creating training table"
    c.execute('''
        CREATE TABLE IF NOT EXISTS training AS
            SELECT DISTINCT 
                file as file,
                title as title,
                author as author,
                books.category as category,
                total as total,
                diff as diff,
                word as word,
                tf as tf
            FROM books NATURAL JOIN book_words
            INNER JOIN indicators USING (word)
        ''')

cat_analysis()
relevance()
indicators()
training_table()
conn.commit()
