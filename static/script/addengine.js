$("#addengine").click(function(event) {
  event.preventDefault();
  var host = $(this).attr("data-host");
  window.external.AddSearchProvider(host + "/opensearchdescription.xml");
});
