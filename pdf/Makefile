TREES =   $(shell find . -iname "*_*_*.pdf" -printf "%f\n" | grep -v - | sed 's/\.pdf//' | sort -u)
SIZES =   $(shell find . -iname "*_*_*.pdf" -printf "%f\n" | grep -v - | sed 's/_[^_]*\.pdf//' | sort -u)
CLASSES = $(shell find . -iname "*_*_*.pdf" -printf "%f\n" | grep -v - | sed 's/_[^_]*_[^_]*\.pdf//' | sort -u)

all: $(addsuffix -all.pdf,$(CLASSES))

%-a4.pdf: %.pdf
	pdfjam -o $@ --paper a4paper $<

%-stamped.pdf: %-a4.pdf
	~/booker/add_side_stamp.py \
		-p A4 \
		--text $* \
		-s 52 \
		$< $@

define NUP_RULE
$(1)-nup.pdf: $$(addsuffix -stamped.pdf,$$(filter $(1)_%,$$(TREES)))
	pdfnup -o $$@ \
		--no-landscape \
		--frame true \
		--scale 0.95 \
		--paper a4paper \
		--nup 5x5 \
		$$^
endef
$(foreach v,$(SIZES),$(eval $(call NUP_RULE,$(v))))

define ALL_RULE
$(1)-all.pdf: $$(addsuffix -nup.pdf,$$(filter $(1)_%,$$(SIZES)))
	pdfjoin -o $$@ \
		$$^
endef
$(foreach v,$(CLASSES),$(eval $(call ALL_RULE,$(v))))

clean:
	$(RM) *-a4.pdf
	$(RM) *-stamped.pdf
	$(RM) *-nup.pdf
	$(RM) *-all.pdf

.PRECIOUS: %-a4.pdf
.PRECIOUS: %-stamped.pdf
.PRECIOUS: %-nup.pdf
.PRECIOUS: %-all.pdf
