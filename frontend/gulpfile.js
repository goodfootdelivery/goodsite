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

// Sass Source & Target
var SASS = './sass/*.scss'
var STYLE = '../assets/stylesheets'

 
/*
 * Compile & File Sass
 */
gulp.task('sass', function(){
	gulp.src(SASS)
		// Compile Sass
		.pipe(plug.sass().on('error', plug.sass.logError))
		// File in Proper Dir
		.pipe(gulp.dest(STYLE));
});


// Complete
gulp.task('build', ['sass']);
