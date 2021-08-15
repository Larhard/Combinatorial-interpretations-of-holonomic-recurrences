MAIN_TARGET = main.pdf
TARGETS = $(MAIN_TARGET)

PDFVIEWER = zathura

LATEXMK = latexmk
LATEXMKFLAGS = -pdf

all: compile

images::
	$(MAKE) -C images

ready::
	$(RM) ready/*
	$(MAKE) clean
	sed -i 's/documentclass\[.*\]/documentclass[final]/' main.tex
	$(MAKE)
	cp main.pdf ready/beamer.pdf
	$(MAKE) clean
	sed -i 's/documentclass\[.*\]/documentclass[handout,final]/' main.tex
	$(MAKE)
	cp main.pdf ready/handout.pdf
	cp konspekt.pdf ready/konspekt.pdf
	git archive --format zip -o ready/src.zip HEAD

watch: $(MAIN_TARGET)
	$(PDFVIEWER) $< &
	$(LATEXMK) $(LATEXMKFLAGS) -pvc $(<:.pdf=.tex)

compile: $(TARGETS)

%.pdf: %.tex
	$(LATEXMK) $(LATEXMKFLAGS) $<

$(TARGETS): images

clean:
	$(RM) *.aux
	$(RM) *.fdb_latexmk
	$(RM) *.fls
	$(RM) *.log
	$(RM) *.nav
	$(RM) *.out
	$(RM) *.snm
	$(RM) *.toc
	$(RM) *.vrb
	$(RM) $(TARGETS)

.PHONY: all
.PHONY: clean
.PHONY: compile
.PHONY: watch
