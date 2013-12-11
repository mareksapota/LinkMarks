include PressUI/utils/scss.mk

static/style/base.css: $(PRESS_SCSS)

include PressUI/utils/scss_clean.mk
include PressUI/utils/python_clean.mk
include PressUI/utils/pressui.mk

.PHONY: clean
clean: press_clean_css press_clean_python press_clean
