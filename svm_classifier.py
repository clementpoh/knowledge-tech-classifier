#!/usr/bin/env python
import sys

from sklearn import svm
from csv import reader, writer

def read_data(filename):
    samples = []
    for row in reader(open(filename)):
        samples.append(row)
    return samples[1:]

raw_train = read_data("data/train.csv")
raw_test = read_data("data/dev.csv")

targets = [ord(x[2]) for x in raw_train]
train   = [x[3:] for x in raw_train]
test    = [x[3:] for x in raw_test]
meta    = [x[0:3] for x in raw_test]

svc = svm.SVC(probability=True)
svc.fit(train, targets)

classes = list(svc.predict(test))
probs   = list(svc.predict_proba(test))

output = writer(open('svm.csv', 'wb'))
header = ['File', 'Title', 'Actual', 'Predicted']
output.writerow(header)
for i in range(len(test)):
    meta[i].append(chr(int(classes[i])))
    row = meta[i] + list(probs[i])
    output.writerow(row)
