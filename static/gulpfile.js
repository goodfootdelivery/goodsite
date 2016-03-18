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

// Source Variables
var MOBILE = './src/mobile'
var BROWSER = './src/browser'
var SASS = './src/sass/*.scss'
// Dest. Variables
var BUNDLES = './dist/bundles'
var SCRIPTS = './dist/js'
var STYLE = './dist/css'

// pack mobile app
gulp.task('mobile', function(){
	gulp.src(MOBILE)
	.pipe(webpack(
		require('./webpack/webpack.config.mobile.js')
	))
	.pipe(gulp.dest(BUNDLES))
})
 
// pack jquery app
gulp.task('browser', function(){
	gulp.src(BROWSER)
	.pipe(webpack(
		require('./webpack/webpack.config.browser.js')
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
gulp.task('build', ['sass', 'browser']);
