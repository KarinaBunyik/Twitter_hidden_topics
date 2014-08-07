var async = require('async');
var MongoClient = require('mongodb').MongoClient;
var collectionSource;
var collectionDestination;
//var destinationConnectionString = 'mongodb://db1.wndrk.com,db2.wndrk.com,db3.wndrk.com/twitterElection?replicaSet=rs0';
//var sourceConnectionString = 'mongodb://localhost:27017/twitterDestination';
var ConnectionString = 'mongodb://localhost:27017/tweets_by_users';

function transferTweets(){
      var cursor = collectionSource.find({}, {'limit':50}).toArray(function(err, docs) {

        if (docs.length < 1){
            console.log('No more tweets in here :(');
            return;
        }

        async.eachSeries(docs, function( element, callback) {
        // if any of the saves produced an error, err would equal that error
          //console.log(element);
          collectionDestination.save(element,function(err,res){
            collectionSource.remove(element,callback);
          });
          
        },function onFinish(err, res){
            if (err){
                console.log(err);
            }
            //console.log('Finished! ' + docs.length);
            transferTweets();
        });
      });
  }

isArray = function(a) {
    return (!!a) && (a.constructor === Array);
};

function loopExtractTweets(){
  //db.open(function(err, db) {
    //db.collection('Customers', function(err, collection) {
        collectionSource.find(function(err, cursor) {
            cursor.each(function(err, user) {
                //console.log('User found');
                if (isArray(user.text)){
                  async.each(user.text, function( element, callback) {
                      var elementTemp = element;
                      elementTemp._id = element.id;
                      elementTemp.username = user.username;
                      elementTemp.name = user.name;
                      elementTemp.following = user.following;
                      elementTemp.followers = user.followers;
                      elementTemp.location = user.location;
                      elementTemp.username = user.username;
                      elementTemp.userid = user.id;
                      if (user.url){
                        elementTemp.url = user.url;
                      }
                      if (user.description){
                        elementTemp.description = user.description;
                      }
                    collectionDestination.save(elementTemp,callback);
                  },function onFinish(err, res){
                   if (err){
                    console.log(err);
                    }
                });
                }
                else
                  {
                      var elementTemp = user.text;
                      elementTemp._id = element.id;
                      elementTemp.username = user.username;
                      elementTemp.name = user.name;
                      elementTemp.following = user.following;
                      elementTemp.followers = user.followers;
                      elementTemp.location = user.location;
                      elementTemp.username = user.username;
                      elementTemp.userid = user.id;
                      if (user.url){
                        elementTemp.url = user.url;
                      }
                      if (user.description){
                        elementTemp.description = user.description;
                      }
                    collectionDestination.save(elementTemp,callback);
                  }
                  //console.log('Tweet found');
            });
        });
    //});
//});
}


MongoClient.connect(ConnectionString, function(err, db) {
  if (err) throw err;
  console.log("Connected to Database");
  collectionSource = db.collection('twitter-pldebatt-140504');

    MongoClient.connect(ConnectionString, function(err, db) {
      if (err) throw err;
      console.log("Connected to Database");
      collectionDestination = db.collection('twitter-pldebatt-131006_by_tweets');

      loopExtractTweets();
    });
});