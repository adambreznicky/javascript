function makeAlert () {
    alert("ahhh!!!");
}

var angular = require('./node_modules/angular/index.js');
angular.module('catalog', [])
  .controller('TodoController', ['$scope', function ($scope) {
    $scope.todos = [
      { title: 'Learn Javascript', completed: true },
      { title: 'Learn Angular.js', completed: false },
      { title: 'Love this tutorial', completed: true },
      { title: 'Learn Javascript design patterns', completed: false },
      { title: 'Build Node.js backend', completed: false },
    ];
  }]);