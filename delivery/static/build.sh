#!/bin/bash

# Script to move all frontend files to base directories
# To import access

BASE=~/workspace/goodfoot/apps/delivery/static
MODS=$BASE/mods

#If directories exist
if [ -d $BASE/css ] || [ -d $BASE/js ]
then
	test -d $BASE/css && rm -rf $BASE/css
	test -d $BASE/js && rm -rf $BASE/js
	test -d $BASE/fonts && rm -rf $BASE/fonts
fi

# Make new dirs
mkdir $BASE/css && CSS=$BASE/css
mkdir $BASE/js && JS=$BASE/js
mkdir $BASE/fonts && FONTS=$BASE/fonts

echo 'HWER'
#Link files from dependencies

# Angular.js
if [ -d $MODS/angular ]
then
	angular=$MODS/angular
	test -e $angular/angular.min.js && ln $angular/angular.min.js $JS
	test -e $angular/angular-csp.css && ln $angular/angular-csp.css $CSS
fi

# Angular-Resource
if [ -d $MODS/angular-resource ]
then
	ang_res=$MODS/angular-resource
	test -e $ang_res/angular-resource.min.js && ln $ang_res/angular-resource.min.js $JS
fi

# ngAutocomplete
if [ -d $MODS/ngAutocomplete/src ]
then
	ngauto=$MODS/ngAutocomplete/src
	test -e $ngauto/ngAutocomplete.js && ln $ngauto/ngAutocomplete.js $JS
fi

# Angular-Resource
if [ -d $MODS/angular-bootstrap ]
then
	ang_boot=$MODS/angular-bootstrap
	test -e $ang_boot/ui-bootstrap.min.js && ln $ang_boot/ui-bootstrap.min.js $JS
	test -e $ang_boot/ui-bootstrap-tpls.min.js && ln $ang_boot/ui-bootstrap-tpls.min.js $JS
	test -e $ang_boot/ui-bootstrap-csp.css && ln $ang_boot/ui-bootstrap-csp.css $CSS
fi

# Bootstrap
if [ -d $MODS/bootstrap/dist ]
then
	boot=$MODS/bootstrap/dist
	test -e $boot/css/bootstrap.min.css && ln $boot/css/bootstrap.min.css $CSS
	test -e $boot/css/bootstrap-theme.min.css && ln $boot/css/bootstrap-theme.min.css $CSS
	test -e $boot/js/bootstrap.min.js && ln $boot/js/bootstrap.min.js $JS
	test -d $boot/fonts && ln  $boot/fonts/* $FONTS
fi
