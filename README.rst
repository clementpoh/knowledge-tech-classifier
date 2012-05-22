Knowledge Technologies Project II
=================================

I did not use Weka for this, instead choosing top opt to use random forest and
svm implementations from the python scikit package.

The original intention was just to use the random forest, but I did want
something to match it against, hence the SVM, but it was much more of an
afterthought.

Generating Output
-----------------
1) python train.extract.py
2) python dev.extract.py
3) python rf.classifier.py
4) python svm.classifier.py

Output
------
train.extract.py creates:
    data/train.csv

dev.extract.py creates:
    data/dev.csv

rf.classifier.py creates:
    rf.csv

svm.classifier.py creates:
    svm.csv

Important files
---------------
train.extract.py 
Creates the database knowledge.db, parses the training books
and ultimately creates a feature set from them.

dev.extract.py
Taps into the knowledge.db database, and uses the features there to parse the
dev books to create a feature set from them.

rf.classifier.py
Trains the random forest classifier on data/train.csv then takes the feature
vectors in data/dev.csv and generates rf.csv, which contains predictions for
each row in test.csv and their probabilities.


svm.classifier.py
Trains the svm classifier on data/train.csv then takes the feature
vectors in data/dev.csv and generates rf.csv, which contains predictions for
each row in test.csv and their probabilities.

Assumptions
-----------
The classifiers expect the files:
data/dev.csv
data/dev.class
data/train.csv
data/train.class

Dependencies
------------
rf.classifier.py and svm.classifier.py depend on: 
- Python2.7
- scikit-learn
- numpy
- scipy

The department does not have either of Python2.7 nor scikit.  scikit can be
downloaded from:
http://scikit-learn.org/dev/install.html

It's important to note that if being run on Ubuntu the python-scikit package is
out of date and is best installed from the git repository.

Worked on Ubuntu, and Cygwin (Using the windows Python).

Categories
----------
Guesses.
A) Adventure
B) Folktales
C) Crime
D) Mythology
E) Philosophy
F) Politics
G) Science Fiction
H) Wild West
