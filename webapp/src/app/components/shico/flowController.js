(function() {
  'use strict';

  angular
      .module('shico')
      .controller('FlowController', FlowController);

  function FlowController(ConceptService, GraphConfigService) {
    var vm = this;

    vm.doPost = doPost;
    vm.doPrint = doPrint;
    vm.parameters = {
      terms: 'oorlog',
      maxTerms: 5,
      sumDistances: true
    };

    vm.graph = {
      options: GraphConfigService.getConfig('streamGraph'),
      data:    []
    };

    function doPost() {
      var resp = ConceptService.trackConcept(vm.parameters);

      console.log("DoPost of: ");
      console.log(vm.parameters);

      resp.then(function(data) {

        var allYears = [];
        var allWords = new Set();
        angular.forEach(data, function(wordValues, year) {
          allYears.push(year);
          angular.forEach(wordValues, function(weight, word) {
            allWords.add(word);
          });
        });

        // HACK: we must gather these...
        var yearAliasI = {
          1950: "1950_1959",
          1951: "1951_1960",
          1952: "1952_1961",
          1953: "1953_1962"
        };
        var yearAlias = {
          "1950_1959": 1950,
          "1951_1960": 1951,
          "1952_1961": 1952,
          "1953_1962": 1953
        };
        GraphConfigService.setYearAlias(yearAliasI);

        var newData = [];
        angular.forEach(allWords, function(word) {
          var values = [];
          angular.forEach(allYears, function(year) {
            var val = 0;
            if(word in data[year]) {
              val = data[year][word];
            } else {
              val = 0;
            }

            values.push([ yearAlias[year], val]);
          });
          this.push({
            key: word,
            values: values
          });
        }, newData);

        vm.graph.data = newData;
      });
    }

    function doPrint() {
      console.log("Do print of: ");
      console.log(vm.parameters);
    }
  }
})();
