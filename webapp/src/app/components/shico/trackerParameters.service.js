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
      startKey: '',
      endKey: '',
      minDist: 0.1,
      wordBoost: 1.0,
      forwards: true,
      sumDistances: false,
      algorithm: 'adaptive',   //  'adaptive' or 'non-adaptive'
      // Aggregator parameters:
      aggWeighFunction: 'Gaussian',
      aggWFParam: 1,
      aggYearsInInterval: 1,
      aggWordsPerYear: 5,
    };

    vm.availableYears = {
      from: 0, to: 1,
      values: {},
      options: {
        floor: 0,
        ceil: 1,
        step: 1,
        onChange: updateYearKeys
      }
    };

    var service = {
      getParameters: getParameters,
      setParameters: setParameters,
      availableYears: vm.availableYears,
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

    function updateYearKeys() {
      // Copy values from slider to startKey and endKey
      // Slider contains only year (e.g. 1954), while startKey and endKey
      // require the name of the corresponding w2v model (e.g. 1950_1959)
      var yearValues = vm.availableYears.values;
      var idxYearFrom = vm.availableYears.from;
      var idxYearTo = vm.availableYears.to;

      vm.parameters.startKey = yearValues[idxYearFrom];
      vm.parameters.endKey   = yearValues[idxYearTo];
    }
  }
})();
