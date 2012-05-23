.PHONY: all
all:	rf

train:	
		python train.extract.py

test:	train
		python dev.extract.py

rf:		test
		python rf.classifier.py

svm:	test
		python svm.classifier.py
	
.PHONY: all
clean:
		rm rf.csv svm.csv knowledge.db data/dev.csv data/train.csv
