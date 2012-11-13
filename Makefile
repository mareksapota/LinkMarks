%.py : %.tmpl
	cheetah compile --nobackup $<

%.css : %.scss
	sass $< $@

SCSS=$(shell find style/ -type f -name \*.scss)
CSS=$(patsubst %.scss, %.css, $(SCSS))

.PHONY: templates
templates: $(CSS)

.PHONY: clean
clean:
	-rm -f $(shell find . -type f -name \*.py[co])
	-rm -rf $(shell find . -type d -name __pycache__)
	-rm -f $(CSS)
	-rm -rf .sass-cache
