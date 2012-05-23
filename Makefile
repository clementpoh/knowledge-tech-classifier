TRAIN	=	train.extract.py
TRAIN_D	=	data/train.csv
TEST	=	dev.extract.py 
TEST_D	=	data/dev.csv


.PHONY: all
all:	rf

train:	$(TRAIN)
		python $(TRAIN)

test:	$(TEST) train
		python $(TEST)

rf:		train test
		python rf.classifier.py

svm:	test
		python svm.classifier.py
	
.PHONY: all
clean:
		rm rf.csv svm.csv knowledge.db data/dev.csv data/train.csv report/report.log report/report.aux
