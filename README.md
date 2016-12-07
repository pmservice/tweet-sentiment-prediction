# About

### Description:

This guide will help you to explain steps necessary to deploy streaming service on [IBM Watson Machine Learning Bluemix][1] offering. 

Streaming service uses Watson Machine Learning REST API to deploy models and work with streaming data which is provided by BlueMix MessageHub service.
By using streaming service, you can:
- Deploy models which are developed by Data Scientists by providing model info, MessageHub and Apache Spark Service details.
- Get status of your existing deployments.
- Start/Stop/Delete specific streaming deployment.

In order to create MessageHub and Apache Spark services, you should login to [IBM Bluemix][2] and click on Catalog to see available services. See [free trial][3] if you don't yet have an ID.


![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/catalog.png)

You can search for MessageHub and Apache Spark services and create as per below instructions.

MessageHub Service;

![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/ms_catalog.png)
  
![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/ms_service.png)  


Apache Spark Service;

![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/as_catalog.png)
  
![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/as_service.png)  


# Preparing MessageHub 

Once you have MessageHub service up and running, you need to create topic for you streaming deployment.

- From the Bluemix dashboard, click on MessageHub service you have created.

![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/dashboard.png)  

- Create topics by clicking on “+” sign. For streaming deployment, you need one input and one output topic.

![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/messagehub_topics.png)

- Once you have your topics ready, you can use kafka rest url and your api key to retrieve the list of topic by using cURL calls from Apache Spark Notebooks. 
Kafka REST URL and Api Key information are provided in service credentials.

![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/messagehub_sc.png)


# Apache Spark Service Credentials

Once you have your Apache Spark service up and running, you can check your service credentials.
From Dashboard, click on Spark service you have created

![sample_output](https://github.com/pmservice/tweet-sentiment-prediction/blob/master/images/dashboard_as.png)

Click on “Service Credentials”


# cURL Statements to Interact with MessageHub

In order to push messages to your kafka topic you can use provided sample python script here:  

https://github.com/pmservice/tweet-sentiment-prediction/blob/master/script/KafkaProducer.py

To use the script, you need to provide your own service credentials.

In order to read what you sent to MessageHub, you can also use curl command to create kafka consumer and read from one of your topics.

### Example request for consumer creation:

#### consumer for input topic
curl -X POST -H "Content-Type: application/vnd.kafka.v1+json" \
-H "X-Auth-Token: gkyIt44JC9S1eGDvPtg1KfpKcbWd2FdtaN8ExRZKYNjQgfr5" \
--data '{"name": "my_consumer_instance", "format": "binary", "auto.offset.reset": "smallest"}' \
https://kafka-rest-prod01.messagehub.services.us-south.bluemix.net:443/consumers/my_json_consumer 

#### consumer for output topic
curl -X POST -H "Content-Type: application/vnd.kafka.v1+json" \
-H "X-Auth-Token: gkyIt44JC9S1eGDvPtg1KfpKcbWd2FdtaN8ExRZKYNjQgfr5" \
--data '{"name": "my_output_consumer_instance", "format": "binary", "auto.offset.reset": "smallest"}' \
https://kafka-rest-prod01.messagehub.services.us-south.bluemix.net:443/consumers/my_json_consumer 

### Example response:
{'base_uri': 'https://kafka-rest-prod01.messagehub.services.us-south.bluemix.net:443/consumers/my_json_consumer/instances/my_consumer_instance',
 'instance_id': 'my_consumer_instance'}
 
### Reading from input topic with created consumer;
curl -X GET -H "Accept: application/vnd.kafka.v1+json" \
-H "X-Auth-Token: gkyIt44JC9S1eGDvPtg1KfpKcbWd2FdtaN8ExRZKYNjQgfr5" \
https://kafka-rest-prod01.messagehub.services.us-south.bluemix.net:443/consumers/my_json_consumer/instances/my_consumer_instance/topics/_StreamingInput

### Example response:
{"key":null,"value":"c2FtcGxlIHR3ZWV0Cg==","partition":0,"offset":402}

Depending on the type of the message, you may receive messages in binary format. You can convert binary messages to readable format by using command line

$ echo "c2FtcGxlIHR3ZWV0Cg==" | base64 -D

$ "sample tweet"


### Reading from output topic with created consumer;
curl -X GET -H "Accept: application/vnd.kafka.binary.v1+json" \
-H "X-Auth-Token: gkyIt44JC9S1eGDvPtg1KfpKcbWd2FdtaN8ExRZKYNjQgfr5" \
https://kafka-rest-prod01.messagehub.services.us-south.bluemix.net:443/consumers/my_json_consumer/instances/my_output_consumer/topics/_StreamingOutput


### Example response:
[{"key":null,"value":"eyJ0d2VldCI6InNhbXBsZSB0d2VldCIsInR3ZWV0X3dvcmRzIjpbInNhbXBsZSIsInR3ZWV0Il0sIndvcmRzIjpbInNhbXBsZSIsInR3ZWV0Il0sImZlYXR1cmVzIjp7InR5cGUiOjAsInNpemUiOjI2MjE0NCwiaW5kaWNlcyI6WzE0OTEwNSwyMjY3MzBdLCJ2YWx1ZXMiOlsxLjAsMS4wXX0sInJhd1ByZWRpY3Rpb24iOnsidHlwZSI6MSwidmFsdWVzIjpbLTIzLjg1ODkxNDgyNTQ2ODUxNywtMjQuMDA3MDM0NTA3NDY1MTFdfSwicHJvYmFiaWxpdHkiOnsidHlwZSI6MSwidmFsdWVzIjpbMC41MzY5NjIzNjczOTI0OTU0LDAuNDYzMDM3NjMyNjA3NTA0Nl19LCJwcmVkaWN0aW9uIjowLjB9","partition":0,"offset":13}]

#### Decode response:
echo "eyJ0d2VldCI6InNhbXBsZSB0d2VldCIsInR3ZWV0X3dvcmRzIjpbInNhbXBsZSIsInR3ZWV0Il0sIndvcmRzIjpbInNhbXBsZSIsInR3ZWV0Il0sImZlYXR1cmVzIjp7InR5cGUiOjAsInNpemUiOjI2MjE0NCwiaW5kaWNlcyI6WzE0OTEwNSwyMjY3MzBdLCJ2YWx1ZXMiOlsxLjAsMS4wXX0sInJhd1ByZWRpY3Rpb24iOnsidHlwZSI6MSwidmFsdWVzIjpbLTIzLjg1ODkxNDgyNTQ2ODUxNywtMjQuMDA3MDM0NTA3NDY1MTFdfSwicHJvYmFiaWxpdHkiOnsidHlwZSI6MSwidmFsdWVzIjpbMC41MzY5NjIzNjczOTI0OTU0LDAuNDYzMDM3NjMyNjA3NTA0Nl19LCJwcmVkaWN0aW9uIjowLjB9" |base64 -D

#### Decoded output:
{"tweet":"sample tweet","tweet_words":["sample","tweet"],"words":["sample","tweet"],"features":{"type":0,"size":262144,"indices":[149105,226730],"values":[1.0,1.0]},"rawPrediction":{"type":1,"values":[-23.858914825468517,-24.00703450746511]},"probability":{"type":1,"values":[0.5369623673924954,0.4630376326075046]},"prediction":0.0}


# License

  
  [Apache 2.0][4]


[1]: https://console.ng.bluemix.net/catalog/services/ibm-watson-machine-learning/
[2]: https://console.ng.bluemix.net/
[3]:  http://www.ibm.com/developerworks/cloud/library/cl-bluemix-fundamentals-start-your-free-trial/index.html
[4]: http://www.apache.org/licenses/LICENSE-2.0.html
