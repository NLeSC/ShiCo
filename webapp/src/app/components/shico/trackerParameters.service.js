(function() {
  'use strict';

  angular
    .module('shico')
    .service('TrackerParametersService', TrackerParametersService);

  function TrackerParametersService() {
    var vm = this;

    vm.parameters = {
      terms: 'oorlog',
      maxTerms: 10,
      maxRelatedTerms: 10,  // TO BE INCLUDED
      startKey: '',         // TO BE INCLUDED
      endKey: '',           // TO BE INCLUDED
      minDist: 0.0,         // TO BE INCLUDED
      wordBoost: 1.0,       // TO BE INCLUDED
      forwards: true,       // TO BE INCLUDED
      sumDistances: false,  // TO BE INCLUDED
      algorithm: 'inlinks', // TO BE INCLUDED
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
