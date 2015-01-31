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
var city_code;
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
      res.send(docs);
      console.log(docs._id);
    }else{
      console.log(e);
      res.send("Failed! Please check Console errors");
    }

  })
})



app.get('/cleaned_chat/logs/find_tags_by_city/:city_code',function(req,res){
  console.log("Inside Find By City Code");
   city_code=req.params.city_code.valueOf();
  // db.collection('cleaned_chats').find({"chat_city":Math.round(city_code)},{"tag":1,"_id":0}).toArray(function(e,docs){
  //   if(!e){
  //     res.send(docs);
  //   }else{
  //     console.log(e);
  //     res.send("Failed!Please Check Console Errors");
  //   }
  // })
//});
db.collection('cleaned_chats').aggregate([
{$match: { "chat_city": Math.round(city_code)}},  
{$unwind: "$tag"},  
{$group: {_id:{'tag':"$tag"},
           num_tags:{$sum:1}}}
],function(e,docs){
  if(!e){
    res.send(docs);
  }else{
    console.log(e);
    res.send("Failed");
  }
}) 
              

})







// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);