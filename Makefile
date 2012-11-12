%.py : %.tmpl
	cheetah compile --nobackup $<

%.css : %.scss
	sass $< $@

TMPL=$(shell find templates/ -type f -name \*.tmpl)
PYTMPL=$(patsubst %.tmpl, %.py, $(TMPL))

SCSS=$(shell find style/ -type f -name \*.scss)
CSS=$(patsubst %.scss, %.css, $(SCSS))

.PHONY: templates
templates: $(PYTMPL) $(CSS)

.PHONY: clean
clean:
	-rm -f $(shell find . -type f -name \*.py[co])
	-rm -f $(CSS) $(PYTMPL)
	-rm -rf .sass-cache
