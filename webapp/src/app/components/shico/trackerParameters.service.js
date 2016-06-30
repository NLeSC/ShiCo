(function() {
  'use strict';

  angular
    .module('shico')
    .service('TrackerParametersService', TrackerParametersService);

  function TrackerParametersService($http, marked) {
    var vm = this;

    vm.parameters = {
      terms: '',
      maxTerms: 10,
      maxRelatedTerms: 10,
      startKey: '',
      endKey: '',
      minSim: 0.5,
      wordBoost: 1.0,
      forwards: 'Forward',
      boostMethod: 'Sum similarity',
      algorithm: 'Adaptive',   //  'adaptive' or 'non-adaptive'
      // Aggregator parameters:
      aggWeighFunction: 'Gaussian',
      aggWFParam: 1,
      aggYearsInInterval: 2,
      aggWordsPerYear: 5,
      doCleaning: 'No'
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

    vm.features = {
      canClean: false
    }

    // Load tool tips for all parameters
    vm.tooltips = {};
    loadToolTip('/help/seedConcept.md'    , 'seedConcept');
    loadToolTip('/help/maxTerms.md'       , 'maxTerms');
    loadToolTip('/help/maxRelatedTerms.md', 'maxRelatedTerms');
    loadToolTip('/help/minSim.md'         , 'minSim');
    loadToolTip('/help/wordBoost.md'      , 'wordBoost');
    loadToolTip('/help/boostMethod.md'    , 'boostMethod');
    loadToolTip('/help/algorithm.md'      , 'algorithm');
    loadToolTip('/help/direction.md'      , 'direction');
    loadToolTip('/help/yearsInInterval.md', 'yearsInInterval');
    loadToolTip('/help/wordsPerYear.md'   , 'wordsPerYear');
    loadToolTip('/help/weighFunc.md'      , 'weighFunc');
    loadToolTip('/help/wFParam.md'        , 'wFParam');
    loadToolTip('/help/doCleaning.md'     , 'doCleaning');
    loadToolTip('/help/yearPeriod.md'     , 'yearPeriod');

    var service = {
      getParameters: getParameters,
      setParameters: setParameters,
      tooltips: vm.tooltips,
      availableYears: vm.availableYears,
      features: vm.features
    };
    return service;

    function getParameters() {
      return vm.parameters;
    }

    function setParameters(params) {
      // Copy parameters from `params` which already exist in `vm.parameters`
      angular.forEach(vm.parameters, function(val,key) {
        if(angular.isDefined(params[key])) {
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

    function loadToolTip(url, ttKey) {
      $http({method: 'GET',url: url})
        .success(function(content){
            vm.tooltips[ttKey] = marked(content);
        });
    }
  }
})();
