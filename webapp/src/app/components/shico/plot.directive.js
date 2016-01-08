(function() {
  'use strict';

  angular
    .module('shico')
    .directive('plotDirective', plotDirective);

  function plotDirective() {
    var directive = {
      templateUrl: '/app/components/shico/plotDirective.template.html',
    };
    return directive;
  }
})();
