$("#addengine").click(function(event) {
  event.preventDefault();
  var host = $(this).attr("data-host");
  var token = $(this).attr("data-token");
  window.external.AddSearchProvider(
    host + "/opensearchdescription.xml?token=" + token
  );
});
