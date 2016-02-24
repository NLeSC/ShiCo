(function() {
  'use strict';

  angular
    .module('shico')
    .controller('TrackerGraphsController', TrackerGraphsController);

  function TrackerGraphsController(GraphControlService) {
    var vm = this;

    // Share graph data from service to controller
    // so directive can find them.
    vm.streamGraph = GraphControlService.streamGraph;
    vm.forceGraph = GraphControlService.forceGraph;
    vm.slider_options = GraphControlService.slider_options;
    vm.downloadData = downloadData;

    function downloadData() {
      var rawData = GraphControlService.getRawData().stream;

      // allWords and allYears we already had -- we shouldn't need to build them again
      var allWords = new Set();
      var allYears = [];
      angular.forEach(rawData, function(wordValues, year) {
        allYears.push(year);
        angular.forEach(wordValues, function(weight, word) {
          allWords.add(word);
        });
      });

      // Create CSV file
      var headers = [ '' ].concat(allYears);
      var csvData = [ headers ];
      angular.forEach(allWords, function(word) {
        var row = [ word ];
        angular.forEach(allYears, function(year) {
          var val = (word in rawData[year]) ? rawData[year][word] : 0;
          this.push(val);
        }, row);
        this.push(row);
      }, csvData);

      return csvData;
    }
  }
})();
