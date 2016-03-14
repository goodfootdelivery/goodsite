/**
 * Goodfoot FrontEnd TaskRunner
 *
 *		Fri 29 Jan 12:35:31 2016
 */
'use strict';

// Requirements
var gulp = require('gulp');
var gulpLoadPlugins = require('gulp-load-plugins');
var webpack = require('webpack-stream')
var plug = gulpLoadPlugins();

// File and Dir Variables
var MOBILE = './mobile/index'
var JQUERY = './jquery/index'
var BUNDLES = '../assets/bundles'
var SCRIPTS = '../assets/scripts'
var SASS = './sass/*.scss'
var STYLE = '../assets/stylesheets'

// pack mobile app
gulp.task('mobile', function(){
	gulp.src(MOBILE)
	.pipe(webpack(
		require('./webpack.config.mobile.js')
	))
	.pipe(gulp.dest(BUNDLES))
})
 
// pack jquery app
gulp.task('jquery', function(){
	gulp.src(JQUERY)
	.pipe(webpack(
		require('./webpack.config.jquery.js')
	))
	.pipe(gulp.dest(SCRIPTS))
})
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
gulp.task('build', ['sass', 'pack']);
