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
    var tags = bookmarkTagsString($('#press-form-tags').val());
    if (tags === null) {
      tags = '';
    }
    var objectId = $('#press-form-objectId').val();
    if (objectId === '') {
      objectId = null;
    }
    var data = {
      objectId: $('#press-form-objectId').val(),
      name: $('#press-form-name').val(),
      url: $('#press-form-url').val(),
      keyword: $('#press-form-keyword').val(),
      suggestions_url: $('#press-form-suggestions_url').val(),
      tags: tags
    }
    function onError() {
      $('#press-form-error').text('Save failed');
    }
    $.ajax({
      url: '/save.json',
      type: 'POST',
      data: data,
      success: function(ret) {
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
    return (
      <PressForm
        onSubmit={this.handleSubmit}
        submitLabel={this.props.submitLabel}
        items={content}
      >
        <input
          id='search-form-objectId'
          type='hidden'
          name='objectId'
          value={this.props.objectId}
        />
        <PressFormInput
          label='Name'
          name='name'
          value={this.props.name}
        />
        <PressFormInput
          label='URL'
          name='url'
          value={this.props.url}
        />
        <PressFormInput
          label='Keyword'
          name='keyword'
          value={this.props.keyword}
        />
        <PressFormInput
          label='Tags'
          name='tags'
          value={bookmarkTagsString(this.props.tags)}
        />
        <PressFormInput
          label='Suggestions URL'
          name='suggestions_url'
          value={this.props.suggestions_url}
        />
      </PressForm>
    );
  }
});
