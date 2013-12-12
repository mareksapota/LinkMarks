var cached_prefetch = (function() {
  var cache = {};
  return function(url) {
    if (cache[url] === undefined) {
      cache[url] = true;
      press_prefetch(url);
    }
  };
})();

$(document).on("mouseenter", ".bookmark", function(event) {
  var url = $(this).find(".url a").attr("href");
  cached_prefetch(url);
});
