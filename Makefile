include PressUI/utils/scss.mk

static/style/all.css: $(PRESS_SCSS)

include PressUI/utils/scss_clean.mk
include PressUI/utils/python_clean.mk

.PHONY: clean
clean: press_clean_css press_clean_python
