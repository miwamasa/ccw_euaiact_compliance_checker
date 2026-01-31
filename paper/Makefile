# Makefile for Decision Tree Optimization Paper

MAIN = decision_tree_optimization
LATEX = pdflatex
BIBTEX = bibtex

.PHONY: all clean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc
	rm -f $(MAIN).bbl $(MAIN).blg $(MAIN).nav $(MAIN).snm
	rm -f *.aux *.log *.out

distclean: clean
	rm -f $(MAIN).pdf

# Docker compilation (if TeX not installed locally)
docker:
	docker run --rm -v $(shell pwd):/work -w /work texlive/texlive \
		pdflatex $(MAIN).tex && \
	docker run --rm -v $(shell pwd):/work -w /work texlive/texlive \
		pdflatex $(MAIN).tex
