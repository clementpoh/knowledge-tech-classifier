SRC		=	report.tex
AUX		=	$(SRC:.tex=.aux)
BIB		=	sample.bib


report.pdf: $(SRC) $(BIB)
	pdflatex $(SRC)
	bibtex $(AUX)
	pdflatex $(SRC)

.PHONY: clean
clean: 
	rm report.aux report.bbl report.blg report.log 
