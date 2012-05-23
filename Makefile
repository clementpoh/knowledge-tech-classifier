TRAIN	=	train.extract.py
TRAIN_D	=	data/train.csv
TEST	=	dev.extract.py 
TEST_D	=	data/dev.csv
RF		=	rf.classifier.py
SVM		=	svm.classifier.py
REPORT	=	report/report.tex


.PHONY: all
all:	rf report

train:	$(TRAIN)
		python $(TRAIN)

test:	$(TEST) train
		python $(TEST)

rf:		$(RF) train test
		python $(RF)

svm:	$(SVM) train test
		python $(SVM)

report:	$(REPORT)
		pdflatex $(REPORT)
	
.PHONY: all
clean:
		rm rf.csv svm.csv knowledge.db data/dev.csv data/train.csv report/report.log report/report.aux
