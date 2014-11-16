var newController = function() {
  var content =
    <BookmarkEdit
      name={''}
      url={''}
      keyword={''}
      suggestionsUrl={''}
      tags={''}
      objectId={''}
      submitLabel='Create'
    />;
  return {
    'toolbar':
      <div>
        <PressNavigationButton
          label='Back'
          uri='/'
          className='press-right'
        />
        <h1>New bookmark</h1>
      </div>,
    'content': <PressCard content={content}/>
  };
}
