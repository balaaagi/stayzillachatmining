###StayZilla Hackathon Data Cleaning and Implementation

####Data Cleaning
*Use the datadump in the data folder
		run in terminal python clean_data.py

*Ensure that MongoDB is running 

This script cleans the data and inserts into the mongoDB


####Node API
		run npm install
		run node server.js


Access the following urls patterns for various api
The node app runs in localhost @ port 3080

* 		/cleaned_chat/logs
*		/cleaned_chat/logs/find_tag_count
*		/cleaned_chat/logs/find_tag_count_time
*		/cleaned_chat/logs/find_tags_by_city/<city code>