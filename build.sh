#!/bin/bash

# Script to move all frontend files to base directories
# To import access

BASE=~/workspace/goodfoot/goodfoot/static
MODS=$BASE/mods

# Target Folders
CSS=$BASE/css
JS=$BASE/js
FONTS=$BASE/fonts

#Link files from dependencies

# Angular.js
if [ -d $MODS/angular ]
then
	angular=$MODS/angular
	test -e $angular/angular.min.js && ln -s $angular/angular.min.js $JS
	test -e $angular/angular-csp.css && ln -s $angular/angular-csp.css $CSS
fi

# Angular-Resource
if [ -d $MODS/angular-resource ]
then
	ang_res=$MODS/angular-resource
	test -e $ang_res/angular-resource.min.js && ln -s $ang_res/angular-resource.min.js $JS
fi

# ngAutocomplete
if [ -d $MODS/ngAutocomplete/src ]
then
	ngauto=$MODS/ngAutocomplete/src
	test -e $ngauto/ngAutocomplete.js && ln -s $ngauto/ngAutocomplete.js $JS
fi

# Angular-Resource
if [ -d $MODS/angular-bootstrap ]
then
	ang_boot=$MODS/angular-bootstrap
	test -e $ang_boot/ui-bootstrap.min.js && ln -s $ang_boot/ui-bootstrap.min.js $JS
	test -e $ang_boot/ui-bootstrap-tpls.min.js && ln -s $ang_boot/ui-bootstrap-tpls.min.js $JS
	test -e $ang_boot/ui-bootstrap-csp.css && ln -s $ang_boot/ui-bootstrap-csp.css $CSS
fi

# Bootstrap
if [ -d $MODS/bootstrap/dist ]
then
	boot=$MODS/bootstrap/dist
	test -e $boot/css/bootstrap.min.css && ln -s $boot/css/bootstrap.min.css $CSS
	test -e $boot/css/bootstrap-theme.min.css && ln -s $boot/css/bootstrap-theme.min.css $CSS
	test -e $boot/js/bootstrap.min.js && ln -s $boot/js/bootstrap.min.js $JS
	test -d $boot/fonts && ln -s $boot/fonts/* $FONTS
fi
