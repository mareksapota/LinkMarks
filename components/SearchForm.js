var SearchForm = React.createClass({
  propTypes: {
    query: React.PropTypes.string.isRequired,
  },

  handleSubmit: function(data) {
    PressNavigation.switchToUri('/search', {'query': data['query']});
  },

  render: function() {
    return (
      <PressForm
        onSubmit={this.handleSubmit}
        submitLabel='Search'
      >
        <PressFormInput
          type='search'
          name='query'
          value={this.props.query}
          className='press-wide'
        />
      </PressForm>
    );
  }
});
