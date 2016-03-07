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
var APP = './app/index'
var BUNDLES = '../assets/bundles'
var SASS = './sass/*.scss'
var STYLE = '../assets/stylesheets'

gulp.task('pack', function(){
	gulp.src(APP)
	.pipe(webpack(
		require('./webpack.config.js')
	))
	.pipe(gulp.dest(BUNDLES))
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
