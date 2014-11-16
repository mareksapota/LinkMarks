var showAllController = function() {
  $.ajax({
    url: '/show_all.json',
    success: function(data) {
      var bookmarksList = <BookmarkList bookmarks={data}/>;
      React.render(bookmarksList, $('#content').get(0));
      $('#loading-animation').hide();
    },
    error: function() {
      // TODO do something
    },
    dataType: 'json',
  });
  return (
    <div>
      <PressNavigationButton
        label='Back'
        uri='/'
        className='press-right'
      />
      <h1>All bookmarks</h1>
      <PressLoadingAnimation id='loading-animation'/>
      <div id='content'></div>
    </div>
  );
}
