import tweepy, json, boto3
from requests_aws4auth import AWS4Auth

def lambda_handler(event, context):
	ACCESS_TOKEN = '***'
	ACCESS_SECRET = '******'
	CONSUMER_KEY = '******'
	CONSUMER_SECRET = '******'
	l = StdOutListener()
	auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	stream = tweepy.Stream(auth, l)
	sqs = boto3.resource('sqs')
	#queue = sqs.create_queue(QueueName='test1', Attributes={'DelaySeconds': '5'})
	#search = []
	#search.append(event['track'])
	for i in range(0,5000):
		try:
			stream.filter(locations=[-180,-90,180,90])
		except:
			continue
	return 'Hello'




class StdOutListener(tweepy.StreamListener):
    def on_status(self, status):
        json_data = status._json
        user_info = json_data['user']
        if json_data['coordinates'] and json_data['user']['lang']=='en':
        	skimmed = {
                    'text': json_data['text'].lower().encode('ascii','ignore').decode('ascii'),
                    'coordinates': json_data['coordinates']['coordinates']
                    }
        elif json_data['place'] and json_data['user']['lang']=='en':
        	skimmed = {
                    'text': json_data['text'].lower().encode('ascii','ignore').decode('ascii'),
                    'coordinates': json_data['place']['bounding_box']['coordinates'][0][0]
                    }
        data = json.dumps(skimmed)
        queue = sqs.get_queue_by_name(QueueName='test1')
        response = queue.send_message(MessageBody=data)
        return True
	
	def on_error(self, status):
		return status

