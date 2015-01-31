// server.js

// BASE SETUP
// =============================================================================

// call the packages we need
var express    = require('express'); 		// call express
var app        = express(); 				// define our app using express
var bodyParser = require('body-parser');

// configure app to use bodyParser()
// this will let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 3080; 
var mongo=require('mongoskin');
//var db=monk('localhost:27017/mylinks');
var db=mongo.db("mongodb://localhost:27017/chat_logs",{native_parser:true});
var hh={};
var kk={};
var heartObject={}
var xx,yy;
		// set our port

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router(); 				// get an instance of the express Router

router.use(function(req,res,next){
	console.log("Something Happneing");
	next();
});

// test route to make sure everything is working (accessed at GET http://localhost:8080/api)
router.get('/', function(req, res) {
	res.json({ message: 'hooray! welcome to our api!' });	
});

// more routes for our API will happen here

router.route('/api/hotspots')
 .post(function(req,res){


 });

// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /api
app.use('/api', router);




app.get('/', function(req, res) {
  res.send('please select a collection, e.g., /cleaned_chat/logs')
})


app.get('/cleaned_chat/logs',function(req,res){
  console.log("Inside Basic Log Find");
  db.collection('cleaned_chats').find().toArray(function(e,docs){
    if(!e){
      res.send(docs)
    }else{
      console.log(e);
      res.send("Failed! Please check Console errors")
    }

  })
})











// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);