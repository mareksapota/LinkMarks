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

  processData: function(data) {
    var tags = bookmarkTagsString(data['tags']);
    if (tags === null) {
      tags = '';
    }
    data['tags'] = tags;
    if (data['objectId'] === '') {
      data['objectId'] = null;
    }
    return data;
  },

  handleSuccess: function(ret) {
    if (ret.success) {
      PressNavigation.switchToUri('/edit', {'objectId': ret.objectId});
      return true;
    } else {
      return false;
    }
  },

  handleError: function(ret) {
    return 'Save failed';
  },

  render: function() {
    return (
      <PressForm
        processData={this.processData}
        submitLabel={this.props.submitLabel}
        action='/save.json'
        onSuccess={this.handleSuccess}
        onError={this.handleError}
      >
        <PressFormInput
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
