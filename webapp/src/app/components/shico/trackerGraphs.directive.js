(function() {
  'use strict';

  angular
    .module('shico')
    .directive('trackerGraphs', trackerGraphs);

  function trackerGraphs() {
    var directive = {
      scope: {},    // Directive has it's own personal scope
      templateUrl: 'app/components/shico/trackerGraphs.template.html',
      controllerAs: 'vm',
      controller: 'TrackerGraphsController'
    };
    return directive;
  }
})();
