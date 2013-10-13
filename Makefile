SCSS=$(shell find . -type f -name \*.scss)

static/style/base.css: $(SCSS)
	sass static/style/base.scss static/style/base.css

.PHONY: pressui
pressui:
	git clone https://github.com/maarons/pressui.git PressUI

.PHONY: clean
clean:
	-rm -rf $(shell find . -type d -name __pycache__)
	-rm -f $(shell find . -type f -name \*.css)
	-rm -rf .sass-cache
	-rm -rf PressUI
