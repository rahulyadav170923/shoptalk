import apiai
import json
import uuid
import os

CLIENT_ACCESS_TOKEN = os.environ['CLIENT_ACCESS_TOKEN']
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
session_id = uuid.uuid4().hex

def getdata(query):
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = session_id
    request.query = query
    response = request.getresponse()
    data = json.loads(response.read().decode("utf-8"))
    result = {}
    result["action"] = data['result']['action']
    print data['result']
    result["messages"] = data['result']['fulfillment']['messages']
    return result
