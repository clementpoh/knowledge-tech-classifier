#!/usr/bin/env python
import sys

from csv import reader, writer
from sklearn.ensemble import RandomForestClassifier

splits = 2
estimators = 100
features = 100
seed = 1337

def read_data(filename):
    samples = []
    for row in reader(open(filename)):
        samples.append(row)
    return samples

raw_train = read_data("data/train.csv")
raw_test = read_data("data/dev.csv")

targets = [x[2] for x in raw_train]
train   = [x[3:] for x in raw_train]
test    = [x[3:] for x in raw_test]
meta    = [x[0:3] for x in raw_test]
columns = sorted(set(targets))

print "Classifying dev using random forests"
print "Estimators:\t%d"     % estimators
print "Min Splits:\t%d"     % splits
print "Max Features:\t%d"   % features
print "Random Seed:\t%d"    % seed

rf = RandomForestClassifier(
        n_estimators = estimators
        , min_samples_split = splits
        , max_features = features
        , random_state = seed
        , compute_importances = True
        )
rf.fit(train, targets)

classes = list(rf.predict(test))
probs   = list(rf.predict_proba(test))

output = writer(open('rf.csv', 'wb'))
header = ['File', 'Title', 'Actual', 'Predicted'] + columns
output.writerow(header)

correct = 0
for i in range(len(test)):
    meta[i].append(classes[i])
    row = meta[i] + list(probs[i])
    output.writerow(row)

    if classes[i] == meta[i][2]:
        correct += 1

print "%s / %s correctly classified." % (correct, i + 1)
