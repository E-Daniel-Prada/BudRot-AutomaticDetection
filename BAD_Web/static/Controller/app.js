var app = angular.module('app', ['datatables'])
try {
	angular.module('navbarApp')
	app.requires.push('navbarApp');
} catch (err) {
	;
}