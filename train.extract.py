import os, sys
import sqlite3

from csv    import reader, DictWriter
from re     import compile
from math   import log10

PATH = './train/'

# Prepare the db connection
conn = sqlite3.connect('./knowledge.db')
conn.text_factory = str
c = conn.cursor()

r_delims    = compile(r"[\W_\d]+")
r_title     = compile("Title: (.*)")
r_author    = compile("Author: (.*)")

def create_tables():
    print "Creating tables"
    c.execute('''DROP TABLE IF EXISTS words''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS words
            ( word      TEXT PRIMARY KEY
            , freq      INTEGER
            , books     INTEGER
            , idf       REAL
            , UNIQUE    (word)
        )''')

    c.execute('''DROP TABLE IF EXISTS books''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS books
            ( file      TEXT PRIMARY KEY
            , title     TEXT
            , author    TEXT
            , category  TEXT
            , total     INTEGER
            , diff      INTEGER
            , UNIQUE    (file)
        )''')

    c.execute('''DROP TABLE IF EXISTS book_words''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS book_words
            ( file      TEXT
            , word      TEXT
            , freq      INTEGER
            , tf        REAL
            , FOREIGN KEY (file) REFERENCES books(file) ON DELETE CASCADE
        )''') 

def unique_tokens(text):
    total       = 0
    diff        = 0
    words       = {}
    tokens      = r_delims.split(text)
    for t in tokens:
        if len(t) > 3:
            total += 1
            try:
                words[t] += 1
            except:
                diff     += 1
                words[t] = 1.0

    return total, diff, words 


def preprocess_book(file, cat): 
    path = os.path.join(PATH, file)
    text = open(path).read()

    title = r_title.search(text)
    title = title.group(1)[:-1] if title else None

    auth = r_author.search(text)
    auth = auth.group(1)[:-1] if auth else None

    total, diff, tokens = unique_tokens(text.lower())

    c.execute('''INSERT INTO books (file, title, author, category, total, diff)
        VALUES (?, ?, ?, ?, ?, ?)''', [file, title, auth, cat, total, diff])

    print cat, file, total, title, auth
    return tokens, total


def process_books():
    print "Parsing books"
    nbooks = 0.0
    for (file, cat) in reader(open("train.class")):
        tokens, total = preprocess_book(file, cat)

        for (tok, freq) in tokens.items(): 
            c.execute('''INSERT INTO book_words (file, word, freq, tf) VALUES
                (?, ?, ?, ?)''', [file, tok, freq, freq/total])

        nbooks += 1
    return nbooks


def populate_words(nbooks):
    threshold = 10
    print "Calculating idfs for each each term"
    print "appearing in more than %d books" % threshold
    # Get all the words which appear in more than one book.
    c.execute('''SELECT word, sum(freq), count(*) AS books
            FROM book_words
            GROUP BY word
            HAVING books > ?
        ''', [threshold])

    for (word, freq, books) in c.fetchall():
        c.execute('''INSERT INTO words (word, freq, books, idf)
            VALUES (?, ?, ?, ?)''', [word, freq, books, log10(nbooks/books)])
    
def cat_analysis():
    print "Calculating category totals"
    c.execute('''DROP TABLE IF EXISTS categories''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories AS
            SELECT category AS category
                , count(*) AS books
                , sum(total) AS words
            FROM books
            GROUP BY category
        ''')

    print "Calculating category tfs"
    c.execute('''DROP TABLE IF EXISTS cat_words''')
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
    c.execute('''DROP TABLE IF EXISTS relevant''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS relevant AS
            SELECT category AS category
                , word AS word
                , tf * idf AS relevance
            FROM cat_words, words USING (word)
        ''')

def indicators():
    nfeatures = 2000
    plain = False
    print "Selecting top %d indicative words" % nfeatures
    if plain:
        c.execute('''
            CREATE TABLE IF NOT EXISTS indicators AS
                SELECT category AS category
                    , word as word
                    , relevance as score
                FROM relevant
                ORDER BY relevance DESC
                LIMIT ?
            ''', [nfeatures])
    else:
        c.execute('''DROP TABLE IF EXISTS indicators''')
        c.execute('''Create TABLE IF NOT EXISTS indicators
                ( word      TEXT
                , score     REAL
            )''')

        cats = c.execute('SELECT category FROM categories').fetchall()
        ncats = nfeatures / len(cats)
        print "Using top %d words from each category" % ncats
        for (cat,) in cats:
            xs = c.execute('''SELECT word, relevance 
                    FROM relevant 
                    WHERE category = ? 
                    ORDER BY relevance DESC
                    LIMIT ?'''
                , [cat, ncats]).fetchall()
            for x in xs:
                c.execute('''INSERT INTO indicators (word, score)
                    VALUES (?, ?)''', x)

def training_table():
    print "Creating training table"
    c.execute('''DROP TABLE IF EXISTS training''')
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

def write_training_csv():
    meta = ['file', 'title', 'category', 'author', 'length', 'unique']
    indicators = c.execute('SELECT word, 0 FROM indicators').fetchall()
    columns = meta + [w for (w, f) in indicators]

    output = DictWriter(open('train.csv', 'wb'), columns)
    # output.writeheader()

    print "Outputting final training data csv"
    for (file, cat) in reader(open("train.class")):
        row = dict(indicators)
        c.execute('''SELECT author, title, total, diff, word, tf
                FROM training WHERE file = ?''', [file])
        for (author, title, total, unique, word, tf) in c.fetchall():
            row[word] = tf
        
        row['file'] = file
        row['title'] = title
        row['category'] = cat
        row['author'] = len(author) if author else 0
        row['length'] = total
        row['unique'] = unique

        output.writerow(row)


create_tables()
nbooks = process_books()
populate_words(nbooks)
cat_analysis()
relevance()
indicators()
training_table()
conn.commit()
write_training_csv()
