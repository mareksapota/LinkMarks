function bookmarkTagsString(tags) {
  if ($.trim(tags) !== '') {
    tags_list = tags.split(',');
    return $.map(
      tags_list,
      function(tag, _) {
        return $.trim(tag);
      }
    ).join(', ');
  }
  return null;
}

var Bookmark = React.createClass({
  propTypes: {
    objectId: React.PropTypes.string.isRequired,
    name: React.PropTypes.string.isRequired,
    url: React.PropTypes.string.isRequired,
    keyword: React.PropTypes.string,
    suggestionsUrl: React.PropTypes.string,
    tags: React.PropTypes.string.isRequired
  },

  render: function() {
    var suggestions = null;
    if (this.props.suggestionsUrl !== null) {
      suggestions = (
        <span>
          &nbsp;
          suggestions enabled
        </span>
      );
    }
    var keyword = null;
    if (this.props.keyword !== null) {
      keyword = (
        <span className='keyword'>
          &nbsp;
          <span className='press-text-hint'>({this.props.keyword})</span>
          {suggestions}
        </span>
      );
    }
    var tags = 'No tags';
    var tagsStr = bookmarkTagsString(this.props.tags);
    if (tagsStr !== null) {
      tags = <span>Tags: {tagsStr}</span>;
    }
    var editParams = {'objectId': this.props.objectId};
    return (
      <div className='bookmark'>
        <div className='header'>
          <PressNavigationButton
            label='Edit'
            uri='/edit'
            params={editParams}
            className='press-right'
          />
          <div className='name'>
            {this.props.name}
            {keyword}
          </div>
          <div className='press-clear'></div>
        </div>
        <div className='content'>
          <div className='url'>
            <a href={this.props.url}>{this.props.url}</a>
          </div>
          <div className='tags'>
            {tags}
          </div>
        </div>
      </div>
    );
  }
});
