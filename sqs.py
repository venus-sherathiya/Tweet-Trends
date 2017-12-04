import boto3, json
import re
import tweepy
from textblob import TextBlob

#skimmed = {'text': u'good thing i cut you off when i did', 'coordinates': [-91.655009, 30.146096]}

sqs = boto3.resource('sqs')
sns = boto3.client('sns')
#queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

queue = sqs.get_queue_by_name(QueueName='test1')
print queue.url
queue_url = queue.url

topic = sns.create_topic(Name='tweets')
count = 0
#res = sns.subscribe(TopicArn=topic['TopicArn'], Protocol='sqs', Endpoint='arn:aws:lambda:us-east-1:618717933566:function:ElasticSearch')
#print res
messages = set()
while True:
	tweetdata = {}
	msg_list = queue.receive_messages(VisibilityTimeout=1, WaitTimeSeconds=5, MaxNumberOfMessages=1)
	for msg in msg_list:
		count += 1
	    message = json.loads(msg.body)
	    text = message['text']
	    coordinates = message['coordinates']
	    print text
	    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
	    analysis = TextBlob(tweet)
	    if analysis.sentiment.polarity > 0:
	    	sentiment = 'positive'
	    elif analysis.sentiment.polarity == 0:
	    	sentiment = 'neutral'
	    else:
	    	sentiment = 'negative'
	    tweetdata['default'] = 'default'
	    tweetdata['count'] = count
	    tweetdata['text'] = text
	    tweetdata['sentiment'] = sentiment
	    tweetdata['coordinates'] = coordinates
	    tweet_data = json.dumps(tweetdata)
	    print tweetdata
	    response = sns.publish(TopicArn=topic['TopicArn'], Message=tweet_data, Subject='Indexing')
	    print response
	    #sns.subscribe(TopicArn=topic['TopicArn'], Protocol='lambda', Endpoint='ARN of AWS Lambda Function')
	    msg.delete()