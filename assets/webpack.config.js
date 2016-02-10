// required dependencies
var path = require('path')
var webpack = require('webpack')
var bundleTracker = require('webpack-bundle-tracker')

module.exports = {
	// base dir for resolving entry option
	context: __dirname,
	// the entry point we created earlier
	entry: { 
		order: './scripts/index.js', 
		entry: './scripts/entry.js'
	},
	
	output: {
		path: path.resolve('./bundles/'),
		filename: '[name]-[hash].js',
	},
	
	plugins: [
		new bundleTracker({filename: './webpack-stats.json'}),
		new webpack.ProvidePlugin({
			$: 'jquery',
			jQuery: 'jquery',
			'window.jQuery': 'jquery'
		})
	],

	module: {
        loaders: [
            //a regexp that tells webpack use the following loaders on all 
            //.js and .jsx files
            {test: /\.jsx?$/, 
                //we definitely don't want babel to transpile all the files in 
                //node_modules. That would take a long time.
                exclude: /node_modules/, 
                //use the babel loader 
                loader: 'babel-loader', 
                query: {
                    //specify that we will be dealing with React code
                    presets: ['react'] 
                }
            }
        ]
    },
    
    resolve: {
        //tells webpack where to look for modules
        modulesDirectories: ['node_modules'],
        //extensions that should be used to resolve modules
        extensions: ['', '.js', '.jsx'] 
    }   
}

