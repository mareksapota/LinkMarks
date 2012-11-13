%.css : %.scss
	sass $< $@

SCSS=$(shell find style/ -type f -name \*.scss)
CSS=$(patsubst %.scss, %.css, $(SCSS))

.PHONY: templates
templates: $(CSS)

.PHONY: clean
clean:
	-rm -rf $(shell find . -type d -name __pycache__)
	-rm -f $(CSS)
	-rm -rf .sass-cache
