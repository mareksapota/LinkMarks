PressNavigation.setUriMap({
  '/': indexController,
  '/show_all': showAllController,
  '/login': loginController,
  '/add_engine': addEngineController,
  '/search': searchController,
  '/new': newController,
  '/edit': editController
});

$.ajax({
  url: 'http://localhost.maarons.org:8080/fb_login_info.json',
  success: function(data) {
    PressNavigation.setHostname(data['hostname']);

    FB.init({
      'appId': data['app_id'],
      'cookie': true,
      'xfbml': true,
      'status': true,
      'version': 'v2.0',
    });

    FB.getLoginStatus(function(response) {
      if (response.status === 'connected') {
        PressNavigation.switchToCurrentUri();
      } else {
        PressNavigation.renderUri('/login');
        FB.XFBML.parse();
      }
    });
  },
  error: function() {
    // TODO do something
  },
  dataType: 'json',
});
