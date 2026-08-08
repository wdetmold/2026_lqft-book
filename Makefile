# Book build. Requires latexmk + TeX Live.
LATEXMK = latexmk -pdf -interaction=nonstopmode -halt-on-error

.PHONY: all book solutions figures lint clean distclean

all: book

book:
	rm -f solutions-flag.tex
	$(LATEXMK) main.tex

# Instructor build: same manuscript with worked solutions printed.
solutions:
	echo '\solutionstrue' > solutions-flag.tex
	$(LATEXMK) -jobname=main-solutions main.tex
	rm -f solutions-flag.tex

figures:
	$(MAKE) -C figures/src

lint:
	python3 tools/lint_notation.py
	-chktex -q main.tex chapters/*/*.tex

clean:
	latexmk -c -f main.tex 2>/dev/null || true
	rm -f solutions-flag.tex main-solutions.* *.bbl *.ind *.idx *.ilg

distclean: clean
	latexmk -C -f main.tex 2>/dev/null || true
