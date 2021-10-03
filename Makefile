all: article.pdf defense.pdf article_diff.pdf

article.pdf: article/main.pdf
article_diff.pdf: article/diff.pdf
defense.pdf: defense/main.pdf

%.pdf:
	cp $< $@

article/main.pdf article/diff.pdf::
	$(MAKE) -C article release

defense/main.pdf::
	$(MAKE) -C defense all
