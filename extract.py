import os, sys
import sqlite3

from csv    import reader
from re     import compile

PATH = './train/'

# Prepare the db connection
conn = sqlite3.connect('./knowledge.db')
conn.text_factory = str
c = conn.cursor()

delims_r    = compile(r"[\W_\d]+")
title_r     = compile("Title: (.*)")
author_r    = compile("Author: (.*)")

def create_tables():
    c.execute('''DROP TABLE IF EXISTS words''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS words 
            ( word      TEXT PRIMARY KEY
            , freq      INTEGER
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
            , dist      INTEGER
            , UNIQUE    (file)
        )''')

    c.execute('''DROP TABLE IF EXISTS book_words''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS book_words
            ( file      TEXT
            , word      TEXT
            , freq      INTEGER
            , FOREIGN KEY (file) REFERENCES books(file)
            , FOREIGN KEY (word) REFERENCES words(word)
        )''') 

def unique_tokens(text):
    total       = 0
    distinct    = 0
    words       = {}
    tokens      = delims_r.split(text)
    for t in tokens:
        total += 1
        try:
            words[t] += 1
        except:
            words[t] = 1
            distinct += 1
    return total, distinct, words 

def preprocess_book(file, cat): 
    path = os.path.join(PATH, file)
    text = open(path).read()

    title = title_r.search(text)
    title = title.group(1)[:-1] if title else None

    author = author_r.search(text)
    author = author.group(1)[:-1] if author else None

    total, distinct, tokens = unique_tokens(text.lower())

    c.execute('''INSERT INTO books (file, title, author, category, total, dist)
        VALUES (?, ?, ?, ?, ?, ?)''' 
        , [file, title, author, cat, total, distinct])

    return tokens


def process_books():
    for (file, cat) in reader(open("train.class")):
        tokens = preprocess_book(file, cat)

        for (tok, freq) in tokens.items(): 
            c.execute('''INSERT OR REPLACE into words (word, freq) VALUES (?, 
                COALESCE (
                    (SELECT freq FROM words WHERE word = ?), 0) + ?)''',
                [tok, tok, freq]) 
            c.execute('''INSERT INTO book_words (file, word, freq) VALUES
                (?, ?, ?)''', [file, tok, freq])


create_tables()
process_books()

conn.commit()
