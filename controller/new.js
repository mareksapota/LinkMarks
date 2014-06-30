var newController = function() {
  return (
    <div>
      <PressNavigationButton
        label='Back'
        uri='/'
        className='press-right'
      />
      <h1>New bookmark</h1>
      <BookmarkEdit
        name={''}
        url={''}
        keyword={''}
        suggestionsUrl={''}
        tags={''}
        objectId={''}
        submitLabel='Create'
      />
    </div>
  );
}
