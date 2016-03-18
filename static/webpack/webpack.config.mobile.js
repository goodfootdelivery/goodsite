/*
 *
 *
 *			WEBPACK CONFIGURATION
 *
 *							Thu 11 Feb 15:04:26 2016
 *
 *
 *
 */

var path = require('path')
var webpack = require('webpack')
var bundleTracker = require('webpack-bundle-tracker')

module.exports = {
	// base dir for resolving entry option
	context: __dirname,
	// the entry point we created earlier
	entry: { order: '../src/mobile', },
	
	output: {
		path: path.resolve('../../assets/bundles/'),
		filename: '[name]-[hash].js',
	},
	
	plugins: [
		new bundleTracker({filename: './webpack/webpack-stats.json'}),
		// Include jQuery
		// new webpack.ProvidePlugin({
		// 	$: 'jquery',
		// 	jQuery: 'jquery',
		// 	'window.jQuery': 'jquery'
		// })
	],

	module: {
        loaders: [{
			//a regexp that tells webpack use the following loaders on all 
			//.js and .jsx files
			test: /\.jsx?$/, 
			// Exclude loadin node mods for performance
			exclude: /node_modules/, 
			//use the babel loader 
			loader: 'babel-loader', 
			query: {
				//specify that we will be dealing with React code
				presets: ['react', 'es2015'] 
			}
		}]
    },
    
    resolve: {
        //tells webpack where to look for modules
        modulesDirectories: ['node_modules'],
        //extensions that should be used to resolve modules
        extensions: ['', '.js', '.jsx'] 
    }   
}
