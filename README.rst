Knowledge Technologies Project II
=================================

I did not use Weka for this, instead choosing top opt to use random forest and
svm implementations from the python scikit package.

The original intention was just to use the random forest, but I did want
something to match it against, hence the SVM, but it was much more of an
afterthought.

Outline
-------
The system is split into four parts. The former two parts are responsible for
feature extraction and selection. The latter two are for classification.

The first extractor extracts tokens and other data from the training documents.
It analyses the data determines the relevant features to be used for the
classifiers, then outputs the training vectors for the classifiers. 

The second extractor reads the test data, tokenises it and creates the feature
vectors for the test data according to the analysis carried out by the training
extractor. The output specifications for the two extractors are exactly the
same. So they could be used interchangeably.

The classifiers are completely independent of each other, but are made to be
compatible with the feature vectors created by the extractors. The first is is a
random tree classifier. The second is a support vector machine classifier.

The classifiers are completely independent of each other. Both classifiers take
the same data sets as input and write to the same output specification, so can
be used interchangeably. They both output the file names; titles and authors if
they can be found; the actual category; predicted category; and predicted
probabilities for each category are then written to a csv file.

Generating Output
-----------------
Either run the Makefile with the command:

make

Or manually run the commands in the following order:

1) python train.extract.py
2) python dev.extract.py
3) python rf.classifier.py
4) python svm.classifier.py

Output
------
train.extract.py creates:
    ./train.csv

dev.extract.py creates:
    ./dev.csv

rf.classifier.py creates:
    ./rf.csv

svm.classifier.py creates:
    ./svm.csv

When using 500 trees per forest, and 300 features per split, rf.classifier.py
takes around 301.66 seconds on an Ubuntu Core 2 Duo.

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
The classifiers expect the following files to run correctly:
./dev.csv
./dev.class
./train.csv
./train.class

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
