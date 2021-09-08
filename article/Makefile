MAIN_TARGET = main.pdf
MAIN_SRC = $(MAIN_TARGET:.pdf=.tex)
TARGETS = $(MAIN_TARGET)

LAST = $(shell git tag | tail -n 1)
LAST_DATE = $(shell git show $(LAST) -q --format="%ad")

LAST_TARGET = last.pdf
LAST_SRC = $(LAST_TARGET:.pdf=.tex)

DIFF_TARGET = diff.pdf
DIFF_SRC = $(DIFF_TARGET:.pdf=.tex)

PDFVIEWER = zathura

LATEXMK = latexmk
LATEXMKFLAGS = -pdf

LATEXDIFF = latexdiff

all: compile

$(LAST_SRC)::
	git show $(LAST):article/main.tex > $@
	sed -i 's|^.*\\date{.*}.*$$|\\date{$(LAST_DATE) ($(LAST))}|' $@

images:: images_src
	$(MAKE) -C $@

images_src::
	$(MAKE) -C $@

$(DIFF_SRC): $(LAST_SRC) $(MAIN_SRC)
	$(LATEXDIFF) $(LAST_SRC) $(MAIN_SRC) > $@

release: $(DIFF_TARGET) $(LAST_TARGET) $(MAIN_TARGET)

watch: $(MAIN_TARGET)
	$(PDFVIEWER) $< &
	$(LATEXMK) $(LATEXMKFLAGS) -pvc $(<:.pdf=.tex)

compile: $(TARGETS)

$(DIFF_TARGET): LATEXMKFLAGS+=-interaction=nonstopmode -f

%.pdf: %.tex
	$(LATEXMK) $(LATEXMKFLAGS) $<

$(TARGETS): images

check: $(MAIN_SRC)
	aspell check -tex -len $<

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
	$(MAKE) -C images

.PHONY: all
.PHONY: clean
.PHONY: compile
.PHONY: watch
.PHONY: images
.PHONY: images_src
.PHONY: check
