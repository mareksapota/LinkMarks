# What is LinkMarks?

LinkMarks is a bookmarking service that was created in an attempt to allow easy
sharing of bookmarks between multiple browsers or computers.

# How to use it?
Copy `config.template.py` to `config.py` and fill it in.

    ./LinkMarks.py config.py

## Automatic redirects
If you pass `?redirect=yes` as a parameter to LinkMarks search and there is only
one matching result you will be automatically redirected to that page.

# Dependencies
- Python 3.x — LinkMarks will not work with Python 2.
- CherryPy
- SASS
