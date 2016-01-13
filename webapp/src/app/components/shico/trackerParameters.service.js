(function() {
  'use strict';

  angular
    .module('shico')
    .service('TrackerParametersService', TrackerParametersService);

  function TrackerParametersService() {
    var vm = this;

    vm.parameters = {
      terms: '',
      maxTerms: 10,
      maxRelatedTerms: 10,
      //startKey: '',         // TO BE INCLUDED
      //endKey: '',           // TO BE INCLUDED
      minDist: 0.1,
      wordBoost: 1.0,
      forwards: true,
      sumDistances: false,
      algorithm: 'inlinks',   //  'inlinks', 'outlinks', or 'non-adaptive'
      // Aggregator parameters:
      // agg.weighF: 'Gausian',          // TO BE INCLUDED
      // agg.wfParam: 1,         // TO BE INCLUDED
      "agg.yearsInInterval": 1, // TO BE INCLUDED
      // agg.nWordsPerYear,   // TO BE INCLUDED
    };

    var service = {
      getParameters: getParameters,
      setParameters: setParameters,
    };
    return service;

    function getParameters() {
      return vm.parameters;
    }

    function setParameters(params) {
      // Copy parameters from `params` which already exist in `vm.parameters`
      angular.forEach(vm.parameters, function(val,key) {
        if(params[key] !== undefined) {
          vm.parameters[key] = params[key]
        }
      });
    }
  }
})();
