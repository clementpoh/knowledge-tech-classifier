#!/usr/bin/env python
import sys

from csv import reader, writer
from sklearn.ensemble import RandomForestClassifier

def read_data(filename):
    samples = []
    for row in reader(open(filename)):
        samples.append(row)
    return samples[1:]

raw_train = read_data("data/train.csv")
raw_test = read_data("data/dev.csv")

targets = [x[2] for x in raw_train]
train   = [x[3:] for x in raw_train]
test    = [x[3:] for x in raw_test]
meta    = [x[0:3] for x in raw_test]

rf = RandomForestClassifier(
        n_estimators = 100
        , min_split = 2
        , compute_importances = True
        , random_state = 1337
        )
rf.fit(train, targets)

classes = list(rf.predict(test))
probs   = list(rf.predict_proba(test))

output = writer(open('rf.csv', 'wb'))
header = ['File', 'Title', 'Actual', 'Predicted']
output.writerow(header)
for i in range(len(test)):
    meta[i].append(classes[i])
    row = meta[i] + list(probs[i])
    output.writerow(row)
