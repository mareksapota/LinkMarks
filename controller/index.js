var indexController = function(params) {
  var defaultParams = {
    'query': ''
  };
  $.extend(defaultParams, params);
  params = defaultParams;

  var SearchForm = React.createClass({
    handleSubmit: function(event) {
      var query = $('#search-form-input').val();
      PressNavigation.switchToUri('/search', {'query': query});
      event.preventDefault();
    },

    render: function() {
      return (
        <form action='#' onSubmit={this.handleSubmit}>
          {this.props.children}
          <input
            type='submit'
            className="press-right press-button"
            value='Search'
          />
        </form>
      );
    }
  });

  var SearchFormInput = React.createClass({
    getInitialState: function() {
      return {value: params.query};
    },

    handleChange: function(event) {
      this.setState({value: event.target.value});
    },

    render: function() {
      return (
        <input
          id='search-form-input'
          type='search'
          className='press-wide'
          value={this.state.value}
          onChange={this.handleChange}
        />
      );
    }
  });

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
        <SearchForm>
          <SearchFormInput/>
        </SearchForm>
        <PressNavigationButton
          label='Show all bookmarks'
          uri='/show_all'
          className='press-left'
        />
      </div>
  };
}
