var async = require('async');
var fs = require('fs');
var _ = require('underscore');
var MongoClient = require('mongodb').MongoClient;

var connectionString = 'mongodb://localhost:27017/tweets_by_users';
var collectionName = 'twitter-pldebatt-140504';
var filePath = '/Volumes/Data/Twitter_pldebatt_project/Data/Internal/tfidf/representative_words/antirasism.txt';
var stoplistPath = '/Volumes/Data/Twitter_pldebatt_project/Data/Internal/tfidf/representative_words/swedish_stoplist.txt';
var collection;
var words;
var stopwords;
var tags = {'antiracism':0,
            'school':0,
            'tax':0,
            'crime':0,
            'feminism':0,
            'climate':0,
            'immigration':0,
            'health':0,
            'eu':0,
            'defense':0,
            'openborders':0,
            'welfaregains':0};


function isArray(a) {
    return (!!a) && (a.constructor === Array);
}

function intersect(a, b) {
    var t;
    if (b.length > a.length) {
        t = b;
        b = a;
        a = t;
    } // indexOf to loop over shorter
    return a.filter(function (e) {
        if (b.indexOf(e) !== -1) {
            return true;
        }
    });
}

function isInLemma(lemma){
    "use strict";
    var lemma_list = lemma.toString().split("|");
    //console.log(lemma_list);
    if (intersect(lemma_list, words).length > 0){
        return true;
    }
    return false;
}

function loopExtractTweets(callback) {
    var tweet_number = 0;
    var taggedTweets = [];
    var documentNumber = 0;
    var documentsCount = 0;
    var test = [];

    collection.find({}, function (err, docs) {

        if (err) throw err;

        // Count the number of documents
        docs.count(function(err, res){
            "use strict";
            documentsCount = res;
            console.log("Found " + documentsCount + " documents");

            function processUser(err, user) {

                if(err) throw err;
                if(user === null) {
                    callback(null, null);
                    return; // All done!
                }

                documentNumber++;

                //var tweetsToUpdate = [];

                if (user.text && isArray(user.text)) {

                    user.text.forEach(function (tweet) {

                        tweet_number++;

                        // Print progress
                        if(tweet_number % 10000 === 0) {
                            var progress = documentNumber / documentsCount * 100;
                            console.log(progress + "%");
                            console.log('Current number of antiracism tweets: ' + tags.antiracism);
                            console.log(test);
                        }
                        if (tweet.tweettag && (_.contains(tweet.tweettag,  'antiracism'))) {
                            tags.antiracism++ ;
                            console.log('hello');
                        }
                        else if (tweet.tweettag){
                            test.push(tweet.tweettag);
                            console.log('here');
                        }
                    });
                }
/*
                async.eachSeries(tweetsToUpdate, function(tweet, cb) {

                    // Update the database
                    collection.update({'text.id': tweet}, {'$addToSet': {'text.$.tweettags': 'antiracism' }}, function (err, res) {

                        // Call the 'internal' async callback cb() so that async knows
                        // that database has been completed
                        cb(err, res);
                    });

                }, function onFinish(err, res){

                   if(err) throw err;
                    docs.nextObject(processUser);
                });
               */
                docs.nextObject(processUser);
            }

            docs.nextObject(processUser);
        });
    });
}

// Read file to array
fs.readFile(stoplistPath, function(err, data1) {
    "use strict";
    if(err) throw err;
    stopwords = data1.toString().split("\n");

    fs.readFile(filePath, function(err, data2) {

        if(err) throw err;
        words = data2.toString().split("\n");
        console.log("Successfully read in " + words.length + " words");

        // Connect to database
        MongoClient.connect(connectionString, function(err, db) {

		    if (err) throw err;
		    console.log("Connected to Database");
	  	    collection = db.collection(collectionName);

            loopExtractTweets(function onFinish(err, res){
                if (err){
                    throw err;
                }
                console.log('Total number of antiracism tweets: ' + tags.antiracism);
                console.log("Finished " + new Date());
            });
	    });
    });
});