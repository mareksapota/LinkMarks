var editController = function(params) {
  if (params === undefined || params.objectId === undefined) {
    PressNavigation.switchToUri('/');
    return;
  }

  $.ajax({
    url: '/get.json',
    data: {'objectId': params.objectId},
    success: function(bookmark) {
      var editForm = (
        <div>
          <BookmarkEdit
            name={bookmark.name}
            url={bookmark.url}
            keyword={bookmark.keyword}
            suggestionsUrl={bookmark.suggestions_url}
            tags={bookmark.tags}
            objectId={bookmark.objectId}
            submitLabel='Update'
          />
          <PressNavigationButton
            label='Delete'
            uri='/delete'
            params={deleteParams}
            className='press-left'
            onClick={deleteBookmark}
          />
        </div>
      );
      React.render(editForm, $('#content').get(0));
      $('#loading-animation').hide();
    },
    error: function() {
      // TODO do something
    },
    dataType: 'json',
  });

  function deleteBookmark(uri, params) {
    if (confirm("Are you sure?")) {
      $.ajax({
        url: '/delete.json',
        data: {'objectId': params.objectId},
        success: function() {
          PressNavigation.switchToUri('/');
        },
        error: function() {
        },
        dataType: 'json',
        type: 'POST',
      });
    }
    return false;
  }

  var deleteParams = {'objectId': params.objectId};

  var content = (
    <div>
      <div id='content'></div>
      <PressLoadingAnimation id='loading-animation'/>
    </div>
  );
  return {
    'toolbar':
      <div>
        <PressNavigationButton
          label='Back'
          uri='/'
          className='press-right'
        />
        <h1>Edit bookmark</h1>
      </div>,
    'content': <PressCard content={content}/>
  };
}
