$("a.confirm").click(function(event) {
  if (!confirm("Are you sure?")) {
    event.preventDefault();
  }
});
