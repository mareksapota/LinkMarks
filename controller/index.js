var indexController = function(params) {
  var defaultParams = {
    'query': ''
  };
  $.extend(defaultParams, params);
  params = defaultParams;

  return {
    'toolbar':
      <div>
        <PressNavigationButton
          label='Add search engine'
          uri='/add_engine'
          className='press-right'
        />
        <PressNavigationButton
          label='New bookmark'
          uri='/new'
          className='press-right'
        />
        <h1>
          Search your bookmarks
        </h1>
      </div>,
    'content':
      <div>
        <SearchForm query={params.query}/>
        <PressNavigationButton
          label='Show all bookmarks'
          uri='/show_all'
          className='press-left'
        />
      </div>
  };
}
