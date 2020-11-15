# aqi-dingtalk-chatbot
Steps to test the automated Air Quality Index (AQI) via AWS and Dingtalk Chatbot:
1. zip the code (e.g. "zip -r aqi-py.zip .")
2. upload the code to AWS Lambda 
    2.1 make sure to select Python 3.7 
    2.2 in AWS lambda, create an Empty Test event e.g. "{}"
    
 3. Create a Scheduled AWS CloudWatch
    3.1 configure it with fixed schedule of 3 hours
    3.2 target should be the new created AWS Lambda
    
 4. configure the Dingtalk Chatbot function (if not yet done)
