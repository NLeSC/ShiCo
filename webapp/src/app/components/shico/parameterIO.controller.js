(function() {
  'use strict';

  angular
    .module('shico')
    .controller('ParameterIOController', ParameterIOController);

  function ParameterIOController(TrackerParametersService) {
    var vm = this;
    vm.getParameters = getParameters;
    vm.setParameters = setParameters;
    vm.closeParamIO = closeParamIO;

    vm.text = '';
    vm.readOnly = false;
    vm.hide = true;

    function getParameters () {
      vm.hide = false;
      vm.readOnly = true;
      vm.text = JSON.stringify(TrackerParametersService.getParameters());
      vm.btnText = 'Ok';
    }

    function setParameters () {
      vm.hide = false;
      vm.readOnly = false;
      vm.text = '';
      vm.btnText = 'Load';
    }

    function closeParamIO() {
      vm.hide = true;
      if(!vm.readOnly) {
        var params = JSON.parse(vm.text);
        TrackerParametersService.setParameters(params);
      }
    }
  }
})();
