var async = require('async');
var fs = require('fs');
var _ = require('underscore');
var MongoClient = require('mongodb').MongoClient;

var connectionString = 'mongodb://localhost:27017/tweets_by_users';
var collectionName = 'twitter-pldebatt-131006-backup';
var filePath = '/Volumes/Data/Twitter_pldebatt_project/Data/Internal/hashtagPrediction/predicted_tweet_ids.txt';
var stoplistPath = '/Volumes/Data/Twitter_pldebatt_project/Data/Internal/tfidf/representative_words/swedish_stoplist.txt';
var collection;
var words;
var tweet_ids;

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

                var tweetsToUpdate = [];

                if (user.text && isArray(user.text)) {

                    user.text.forEach(function (tweet) {

                        tweet_number++;

                        // Print progress
                        if(tweet_number % 10000 === 0) {
                            var progress = documentNumber / documentsCount * 100;
                            console.log(progress + "% / " + tweet_number + " / " + taggedTweets.length);
                        }

                        tweet.sentence.forEach(function(sent) {
                            sent.w.forEach(function (word) {
                                if (!_.contains(stopwords, word.val) && (_.contains(words, word.val) || (isInLemma(word.lemma.toLowerCase())))) {

                                   // Check if tweet has been taged alrady
                                   if (_.contains(taggedTweets, tweet.id)){
                                       // No need to update database, return
                                       //console.log("Tweet " + tweet.id + " has been tagged already");
                                   }
                                   else {
                                        tweetsToUpdate.push(tweet.id);
                                        taggedTweets.push(tweet.id);
                                   }
                                }
                            });
                        });
                    });
                }

                async.eachSeries(tweetsToUpdate, function(tweet, cb) {

                    // Update the database
                    collection.update({'text.id': tweet}, {'$addToSet': {'text.$.tweettags': 'health' }}, function (err, res) {

                        // Call the 'internal' async callback cb() so that async knows
                        // that database has been completed
                        cb(err, res);
                    });

                }, function onFinish(err, res){

                   if(err) throw err;
                    docs.nextObject(processUser);
                });
            }

            docs.nextObject(processUser);
        });
    });
}

// Read file to array
fs.readFile(filePath, function(err, data1) {
    "use strict";
    if(err) throw err;
    tweet_ids = data1.toString().split("\n");
    console.log("Successfully read in " + tweet_ids.length + " tweet ids.");
    // Connect to database
    MongoClient.connect(connectionString, function(err, db) {
	    if (err) throw err;
		console.log("Connected to Database");
	  	collection = db.collection(collectionName);

        async.eachSeries(tweet_ids, function(tweet, cb) {

            // Update the database
            collection.update({'text.id': tweet}, {'$addToSet': {'text.$.tweettags': 'predicted_nina' }}, function (err, res) {

                // Call the 'internal' async callback cb() so that async knows
                // that database has been completed
                cb(err, res);
            });

        }, function onFinish(err, res){

            if(err) throw err;
                console.log("Finished " + new Date());
        });
    });
 });