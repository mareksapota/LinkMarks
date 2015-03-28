var BookmarkList = React.createClass({
  propTypes: {
    bookmarks: React.PropTypes.array.isRequired,
  },

  render: function() {
    var bookmarks = [];
    $.each(
      this.props.bookmarks,
      function(i, bookmark) {
        bookmarks.push(
          <Bookmark
            key={bookmark.objectId}
            name={bookmark.name}
            url={bookmark.url}
            keyword={bookmark.keyword}
            suggestionsUrl={bookmark.suggestions_url}
            tags={bookmark.tags}
            objectId={bookmark.objectId}
          />
        );
      }
    );
    return (
      <div>
        {bookmarks}
      </div>
    );
  }
});
