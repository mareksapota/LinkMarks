var BookmarkEdit = React.createClass({
  propTypes: {
    objectId: React.PropTypes.string.isRequired,
    name: React.PropTypes.string.isRequired,
    url: React.PropTypes.string.isRequired,
    keyword: React.PropTypes.string,
    suggestionsUrl: React.PropTypes.string,
    tags: React.PropTypes.string.isRequired,
    submitLabel: React.PropTypes.string.isRequired
  },

  handleSubmit: function(event) {
    var tags = bookmarkTagsString($('#search-form-tags').val());
    if (tags === null) {
      tags = '';
    }
    var objectId = $('#search-form-objectId').val();
    if (objectId === '') {
      objectId = null;
    }
    var data = {
      objectId: $('#search-form-objectId').val(),
      name: $('#search-form-name').val(),
      url: $('#search-form-url').val(),
      keyword: $('#search-form-keyword').val(),
      suggestions_url: $('#search-form-suggestions_url').val(),
      tags: tags
    }
    function onError() {
      $('#search-form-error').text('Save failed');
    }
    $.ajax({
      url: '/save.json',
      type: 'POST',
      data: data,
      success: function(ret) {
        console.log(ret);
        if (ret.success) {
          PressNavigation.switchToUri('/edit', {'objectId': ret.objectId});
        } else {
          onError();
        }
      },
      error: function() {
        onError();
      }
    });
    event.preventDefault();
  },

  render: function() {
    var SearchFormInput = React.createClass({
      propTypes: {
        name: React.PropTypes.string.isRequired,
        label: React.PropTypes.string.isRequired,
        value: React.PropTypes.string,
      },

      getInitialState: function() {
        var value = this.props.value;
        if (this.props.value === undefined || this.props.value === null) {
          value = '';
        }
        return {value: value};
      },

      handleChange: function(event) {
        this.setState({value: event.target.value});
      },

      render: function() {
        return (
          <div>
            <label htmlFor={this.props.name}>{this.props.label}</label>
            <input
              id={'search-form-' + this.props.name}
              type='text'
              name={this.props.name}
              value={this.state.value}
              onChange={this.handleChange}
            />
          </div>
        );
      }
    });

    return (
      <form
        className='press-form'
        action='#'
        onSubmit={this.handleSubmit}
      >
        <div id='search-form-error'></div>
        <input
          id='search-form-objectId'
          type='hidden'
          name='objectId'
          value={this.props.objectId}
        />
        <SearchFormInput
          label='Name'
          name='name'
          value={this.props.name}
        />
        <SearchFormInput
          label='URL'
          name='url'
          value={this.props.url}
        />
        <SearchFormInput
          label='Keyword'
          name='keyword'
          value={this.props.keyword}
        />
        <SearchFormInput
          label='Tags'
          name='tags'
          value={bookmarkTagsString(this.props.tags)}
        />
        <SearchFormInput
          label='Suggestions URL'
          name='suggestions_url'
          value={this.props.suggestions_url}
        />
        <input
          type='submit'
          className='press-right press-button'
          value={this.props.submitLabel}
        />
      </form>
    );
  }
});
