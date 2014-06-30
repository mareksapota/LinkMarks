var addEngineController = function() {
  function addEngine() {
    var host = PressNavigation.getHostname();
    window.external.AddSearchProvider(host + "/opensearchdescription.xml");
  }
  return (
    <div>
      <PressNavigationButton
        label="Back"
        uri="/"
        className="press-right"
      />
      <h1>Add LinkMarks search engine</h1>
      <PressButton label='Add' onClick={addEngine}/>
    </div>
  );
}
