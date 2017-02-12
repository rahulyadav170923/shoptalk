import os
from havenondemand.hodclient import *

client = HODClient(os.environ['SENTIMENT_API_KEY'], version="v2")

def sentiment_result(params):
    print (params)
    print (type(params))
    params = {'text': params}
    response = client.get_request(params, HODApps.ANALYZE_SENTIMENT, async=False)
    return response['aggregate']['sentiment']