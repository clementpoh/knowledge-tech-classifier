import os, sys
import sqlite3

from re import split, match, findall

PATH = './train/'

# Prepare the db connection
conn = sqlite3.connect('./knowledge.db')
c = conn.cursor()

def create_table():
    c.execute('''
            CREATE TABLE IF NOT EXISTS words 
                ( word TEXT
                , occurences INTEGER
                , UNIQUE (name)
            )''') 

def unique_tokens(text):
    words = {}
    total = 0
    tokens = split("[\W_\d]+", text)
    for t in tokens:
        if t is not '':
            total += 1
            try:
                words[t][0] += 1
            except:
                words[t] = [1]
    return total, words 

for book in os.listdir(PATH):
    book = os.path.join(PATH, book)
    text = open(book).read().lower()

    total, tokens = unique_tokens(text)
    c.execute('''INSERT INTO words (word, occurences) VALUES (word, 1)''' 
