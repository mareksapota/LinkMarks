# What is LinkMarks?

LinkMarks is a bookmarking service that was created in an attempt to allow easy
sharing of bookmarks between multiple browsers or computers.

# How to use it?
`./LinkMarks.py` will launch LinkMarks in development mode, for production use
`./LinkMarks.py production`.

## Automatic redirects
If you pass `?redirect=yes` as a parameter to LinkMarks search and there is only
one matching result you will be automatically redirected to that page.

# Dependencies
- Python 3.x — LinkMarks will not work with Python 2, this was a concious choice
  made to allow easier development.
- CherryPy
- SQLAlchemy
- Jinja2
- SASS
