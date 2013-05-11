FB.Event.subscribe('auth.authResponseChange', function(response) {
  if (response.status === "connected") {
    window.location.reload(true);
  }
});
