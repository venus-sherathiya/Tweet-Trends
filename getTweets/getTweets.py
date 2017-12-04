import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


def lambda_handler(event, context):
	aws_access_key_id = '******'
	aws_secret_access_key = '******'

	awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, 'us-east-1', 'es')
	host = 'search-tweetmap-gvg5ay73ty4qgtfrytnmlcmhyi.us-east-1.es.amazonaws.com'

	es = Elasticsearch(
	        hosts=[{'host': host, 'port': 443}],
	        use_ssl=True,
	        http_auth=awsauth,
	        verify_certs=True,
	        connection_class=RequestsHttpConnection
	        )

	data = es.search(index="index2",size=4000, body={"query": {"match_all":{"text": event['track']}}}) 
	tweet = []
	for hit in data['hits']['hits']:
		try:
			if hit['_source']:
				tweet.append(hit['_source'])
		except:
			continue
	response_json = json.dumps(tweet)
	return response_json
