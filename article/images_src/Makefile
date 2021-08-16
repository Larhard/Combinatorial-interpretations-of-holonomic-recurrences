SRCS = $(shell find -type f -iname '*.dot')
TARGETS = $(SRCS:.dot=.svg)

all: $(TARGETS)

%.svg: %.dot
	dot -Tsvg -o$@ $<

.PHONY: all
