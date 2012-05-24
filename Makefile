RF		=	rf.classifier.py
PYTHON	=	python27

.PHONY: all
all: rf.csv

train.csv: train.extract.py 
	$(PYTHON) train.extract.py

dev.csv: dev.extract.py train.csv
	$(PYTHON) dev.extract.py

rf.csv: $(RF) train.csv 
	$(PYTHON) $(RF)

svm.csv: svm.classifier.py dev.csv train.csv

.PHONY: clean
clean: 
	rm train.csv dev.csv knowledge.db
