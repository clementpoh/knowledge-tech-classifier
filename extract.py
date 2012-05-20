import os, sys
import sqlite3

from csv    import reader
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS words
            ( word      TEXT PRIMARY KEY
            , freq      INTEGER
            , books     INTEGER
            , idf       REAL
            , UNIQUE    (word)
        )''')

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
    nbooks = 0.0
    for (file, cat) in reader(open("train.class")):
        tokens, total = preprocess_book(file, cat)

        for (tok, freq) in tokens.items(): 
            c.execute('''INSERT INTO book_words (file, word, freq, tf) VALUES
                (?, ?, ?, ?)''', [file, tok, freq, freq/total])

        nbooks += 1
    return nbooks


def populate_words(nbooks):
    # Get all the words which appear in more than one book.
    c.execute('''SELECT word, sum(freq), count(*) AS books
            FROM book_words
            GROUP BY word
            HAVING books > 1
        ''')

    for (word, freq, books) in c.fetchall():
        c.execute('''INSERT INTO words (word, freq, books, idf)
            VALUES (?, ?, ?, ?)''', [word, freq, books, log10(nbooks/books)])
    

create_tables()
nbooks = process_books()
print "Calculating idfs for unique each term."
populate_words(nbooks)

