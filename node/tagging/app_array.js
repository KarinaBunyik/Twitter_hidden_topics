var async = require('async');
var fs = require('fs');
var MongoClient = require('mongodb').MongoClient;

var connectionString = 'mongodb://localhost:27017/tweets_by_users';
var collectionName = 'twitter-pldebatt-130612';
var filePath = '/Volumes/Data/Twitter_pldebatt_project/Data/Internal/tfidf/representative_words/klimat.txt';
var collection;
var words;

function isArray(a) {
    return (!!a) && (a.constructor === Array);
}

function loopExtractTweets(callback) {
    collection.find().toArray(function(err, res){

        if(err) throw err;
        var tweet_ids = [];

        res.forEach(function (user) {

            if (user && user.text && isArray(user.text)) {

                user.text.forEach(function (tweet) {
                    "use strict";
                    tweet.sentence.forEach(function (sent) {
                        sent.w.forEach(function (word) {
                            //console.log(word);
                            if (words.indexOf(word.val) > -1) {
                                console.log(tweet.id);
                                tweet_ids.push(tweet.id);
                            }
                        });
                    });
                });
            }
        });
        callback(null, tweet_ids);
    });

}
/*
                async.each(user.text, function(tweet, callback) {
                    async.each(tweet.sentence, function(sentence, callback) {
                        async.each(sentence.w, function(word, callback) {
                            if (words.indexOf(word.val > -1)) {
                                console.log(tweet._id);
                            }
                            callback(null, null);
                        }, function onFinish(err, res){
                            if (err){
                                console.log(err);
                            }
                            callback(null, null);
                        });

                    }, function onFinish(err, res){
                        if (err){
                            console.log(err);
                        }
                        callback(null, null);
                    });

                }, function onFinish(err, res){
                    if (err){
                        console.log(err);
                    }
                    callback(null, null);
                });
            }
            //console.log('Tweet found');
        });

    });
    //});
//});
}
*/


// Read file to array
fs.readFile(filePath, function(err, data) {
    
    if(err) throw err;

    words = data.toString().split("\n");
    console.log("Successfully read in " + words.length + " words");

    // Connect to database
    MongoClient.connect(connectionString, function(err, db) {

		if (err) throw err;
		console.log("Connected to Database");
	  	collection = db.collection(collectionName);

        var tweet_ids;
        loopExtractTweets(function onFinish(err, tweet_ids){
            if (err){
                throw err;
            }
            collection.update( {'text.id': { '$in': tweet_ids }}, {'$addToSet' : {'text.$.tweettags' : 'climate' }}, function(err,res){
                "use strict";
                if(err) throw err;
                console.log("Finished " + new Date());
            });
        });
	});
});