/**
 * Goodfoot FrontEnd TaskRunner
 *
 *		Fri 29 Jan 12:35:31 2016
 */
'use strict';

// Requirements
var gulp = require('gulp');
var gulpLoadPlugins = require('gulp-load-plugins');
var plug = gulpLoadPlugins();

// Path Variables
var INDEX = './index.html';
var TARG = '.'
// Inject Sources
var JS = './app/**/*.js'
var CSS = './app/**/*.css'
// Sass Source & Target
var SASS = './sass/*.scss'
var STYLE = './stylesheets'


// Inject Custom Deps.
gulp.task('inject', function () {
	gulp.src(INDEX)
		// Bower Injection
		.pipe(plug.wiredep())

		// JS Injection & Angular Sort
		.pipe(plug.inject(
			gulp.src(JS).pipe(plug.angularFilesort())
		))

		// CSS Injection
		.pipe(plug.inject(
			gulp.src(CSS)
		))
		.pipe(gulp.dest(TARG))
});


// Compile & File Sass
gulp.task('sass', function(){
	gulp.src(SASS)
		// Compile Sass
		.pipe(plug.sass().on('error', plug.sass.logError))
		// File in Proper Dir
		.pipe(gulp.dest(STYLE));
});


// Complete
gulp.task('build', ['sass', 'inject']);
