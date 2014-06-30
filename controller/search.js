var searchController = function(params) {
  if (params === undefined || params.query === undefined) {
    PressNavigation.switchToUri('/');
    return;
  }

  $.ajax({
    url: '/search.json',
    data: {'query': params.query},
    success: function(data) {
      $('#loading-animation').hide();
      if (data.keyword) {
        window.location.replace(data.url);
      } else {
        if (params.redirect === 'yes' && data.bookmarks.length === 1) {
          window.location.replace(data.bookmarks[0].url);
          return;
        }
        var bookmarksList = <BookmarkList bookmarks={data.bookmarks}/>;
        React.renderComponent(bookmarksList, $('#content').get(0));
      }
    },
    error: function() {
      // TODO do something
    },
    dataType: 'json',
  });

  var editParams = {'query': params.query};

  return (
    <div>
      <PressNavigationButton
        label='Back'
        uri='/'
        className='press-right'
      />
      <PressNavigationButton
        label='Edit search'
        uri='/'
        params={editParams}
        className='press-right'
      />
      <h1>Search results</h1>
      <PressLoadingAnimation id='loading-animation'/>
      <div id='content'></div>
    </div>
  );
}
