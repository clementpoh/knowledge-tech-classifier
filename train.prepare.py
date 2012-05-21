import os, sys
import sqlite3

from csv import reader, DictWriter

conn = sqlite3.connect('./knowledge.db')
conn.text_factory = str
c = conn.cursor()

meta = ['file', 'category', 'author', 'length', 'unique']
indicators = c.execute('SELECT word, 0 FROM indicators').fetchall()
columns = meta + [w for (w, f) in indicators]

output = DictWriter(open('train.csv', 'wb'), columns)

for (file, cat) in reader(open("train.class")):
    row = dict(indicators)
    c.execute('''SELECT author, total, diff, word, tf
            FROM training WHERE file = ?''', [file])
    for (author, total, unique, word, tf) in c.fetchall():
        row[word] = tf
    
    row['file'] = file
    row['category'] = cat
    row['author'] = author 
    row['length'] = total
    row['unique'] = unique

    output.writerow(row)

