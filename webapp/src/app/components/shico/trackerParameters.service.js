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
      startKey: '',         // TO BE INCLUDED
      endKey: '',           // TO BE INCLUDED
      minDist: 0.1,
      wordBoost: 1.0,
      forwards: true,
      sumDistances: false,
      algorithm: 'inlinks',   //  'inlinks', 'outlinks', or 'non-adaptive'
      // Aggregator parameters:
      aggWeighFunction: 'Gaussian',
      aggWFParam: 1,
      aggYearsInInterval: 1,
      aggWordsYear: 5,
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
      console.log('set startKey and enKey as required...');
      console.log('to values from avlYears.values');
      console.log(vm.availableYears.to);
      console.log(vm.availableYears.values);
      console.log(vm.availableYears.values[vm.availableYears.to]);
    }
  }
})();
