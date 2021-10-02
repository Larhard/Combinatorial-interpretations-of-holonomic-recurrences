SRCS = $(shell find -type f -iname '*.dot')
TARGETS = $(SRCS:.dot=.svg)

DOTFLAGS = -Gbgcolor=transparent -Tsvg

all: $(TARGETS)

%.svg: %.dot
	dot $(DOTFLAGS) -o$@ $<

.PHONY: all
