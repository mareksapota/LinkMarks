# What is LinkMarks?

LinkMarks is a private bookmarking service (or a single user web application if
you prefer) that was created in an attempt to allow easy sharing of bookmarks
between multiple browsers or computers.

# How to use it?
`./LinkMarks.py` will launch LinkMarks in development mode, for production use
`./LinkMarks.py production`.

## Tokens
LinkMarks does not use login and password authentication, instead it uses tokens
— generally single use random strings that can be passed in cookies or in URL.
Tokens are generally single use since LinkMarks supports permanent tokens, you
should have at least one permanent token to make LinkMarks useful.

- `./maketoken.py permanent someLongRandomString`
- Set `https://yourLinkmarksInstance/search?token=someLongRandomString&query=%s`
  as your browser’s search engine.

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
