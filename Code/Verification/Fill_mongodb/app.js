var fs = require('fs');
var xml2object = require('./lib/xml2object');
var MongoClient = require('mongodb').MongoClient;
var metrics = require('measured').createCollection();
var source = fs.createReadStream('../../../../Data/twitter-pldebatt_original.xml');
var numCPUs = require("os").cpus().length;
var collection;

	// Output statistics every 10 seconds
	setInterval(function() {
		console.log(metrics.toJSON());
	}, 10000);

	// Kick off processing
	MongoClient.connect('mongodb://localhost/karinas_twitter_db', function(err, db) {
		if(err) throw err;

		collection = db.collection('nodeTest');

		// Create a new xml parser with an array of xml elements to look for
		var parser = new xml2object([ 'user' ], source);

		// Bind to the object event to work with the objects found in the XML file
		parser.on('object', function(name, obj) {

			saveObject(obj, function(err, result){
				if(err){
					console.log(err);
				}

				updateMetrics();
			});
		});

		// Bind to the file end event to tell when the file is done being streamed
		parser.on('end', function() {
			console.log('Finished parsing xml!');
			db.close();
		});

		// Start parsing the input stream
		parser.start();

		function saveObject(obj, callback){

			if(obj.id !== null){
				obj._id = obj.id;
			}

			collection.save(obj, {safe:true}, function(err, docs) {
				callback(err, docs);
			});
		}

		function updateMetrics(){
			metrics.meter('requestsPerSecond').mark();
		}
	});

