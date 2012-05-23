import os, sys
import sqlite3

from re import compile
from csv import DictWriter, reader

PATH = './dev/'

r_delims    = compile(r"[\W_\d]+")
r_title     = compile("Title: (.*)")
r_author    = compile("Author: (.*)")

conn = sqlite3.connect('./knowledge.db')
conn.text_factory = str
c = conn.cursor()

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

def preprocess_book(file): 
    path = os.path.join(PATH, file)
    text = open(path).read()

    title = r_title.search(text)
    title = title.group(1)[:-1] if title else None

    auth = r_author.search(text)
    auth = auth.group(1)[:-1] if auth else None

    total, diff, tokens = unique_tokens(text.lower())

    print file, total, title, auth
    return tokens, total, diff, title, auth


meta = ['file', 'title', 'category', 'author', 'length', 'unique']
init = c.execute('SELECT word, 0 FROM indicators').fetchall()
indicators = [w for (w, f) in init]
columns = meta + indicators

output = DictWriter(open('data/dev.csv', 'wb'), columns)
print "Outputting test data csv"

for (file, cat) in reader(open("data/dev.class")):
    tokens, total, diff, title, auth = preprocess_book(file)

    row = dict(init)
    for (tok, freq) in tokens.items(): 
        if tok in indicators:
            row[tok] = freq / total
            
    row['file'] = file
    row['title'] = title
    row['category'] = cat
    row['author'] = len(auth) if auth else 0
    row['length'] = total
    row['unique'] = diff

    output.writerow(row)
