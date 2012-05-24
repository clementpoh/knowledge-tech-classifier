PYTHON		=	python
PYTHON27 	=	python27

.PHONY: all
all: rf.csv

train.csv: train.extract.py 
	$(PYTHON) train.extract.py

dev.csv: dev.extract.py train.csv
	$(PYTHON) dev.extract.py

rf.csv: rf.classifier.py train.csv 
	$(PYTHON27) rf.classifier.py

svm.csv: svm.classifier.py dev.csv train.csv
	$(python27) svm.classifier.py

.PHONY: clean
clean: 
	rm train.csv dev.csv knowledge.db
