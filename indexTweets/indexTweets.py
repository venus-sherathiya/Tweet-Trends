from __future__ import print_function
import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

def lambda_handler(event, context):
	aws_access_key_id = '****'
	aws_secret_access_key = '**********'
	awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, 'us-east-1', 'es')
	host = 'search-tweetmap-gvg5ay73ty4qgtfrytnmlcmhyi.us-east-1.es.amazonaws.com'
	es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        use_ssl=True,
        http_auth=awsauth,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )
	tweet = event['Records'][0]['Sns']['Message']
	es.index(index='index2', doc_type='tweet', body=tweet, ignore=[400, 404])
	return tweet
