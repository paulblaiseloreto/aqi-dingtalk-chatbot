import json
from botocore.vendored import requests
import logging

api_url = 'https://api.weatherbit.io/v2.0/current/airquality?city=bejing&key=cdb88e4b86f14e76a93726826d383143'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def post(data):
    webhook_url='https://oapi.dingtalk.com/robot/send?access_token=46aa2f5571f947b73231c160dd8084771db63b23583c6539d44560ff14bed0f5' #the URL to the DingTalk group chatbot
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    post_data = json.dumps(data)
    try:
        response = requests.post(webhook_url, headers=headers, data=post_data)
        logger.info('Send success')
    except requests.exceptions.HTTPError as exc:
        logger.error("Send Error,HTTP error: %d, reason: %s" % (exc.response.status_code, exc.response.reason))
        raise
    except requests.exceptions.ConnectionError:
        logger.error("Send Error, HTTP connection error!")
        raise
    else:
        result = response.json()
        logger.info('Send Error:%s' % result)
        if result['errcode']:
            error_data = {"msgtype": "text", "text": {"content": "Send Error, reason:%s" % result['errmsg']}, "at": {"isAtAll": True}}
            logger.error("Send Error:%s" % error_data)
            requests.post(webhook_url, headers=headers, data=json.dumps(error_data))
        return result
 
# AQI Color
def getColor(aqi):
    if aqi <= 50:
        return "Green"
    elif aqi <= 100:
        return "Yellow"
    elif aqi <= 150:
        return "Orange"
    elif aqi <= 200:
        return "Red"
    elif aqi <= 300:
        return "Purple"
    else:
        return "Maroon" 
        
def prepare_data(title, text, aqi):
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": "Current AQI of Beijing is {}. You're {}".format(aqi, getColor(aqi))
        }
    }
    return data       
        
def callAPI():
    response = requests.get(api_url)    

    if (response.status_code == 200 or response.status_code == 201):
        posts = json.loads(response.text) #load data into a dict of objects, posts
        aqi=posts['data'][0]['aqi'] #store AQI only
        return aqi
    else:
        return None       
        
def lambda_handler(event, context):
    response = callAPI()

    if response is not None:
        data = prepare_data('title', 'text', response)
        post(data)

    else:
        print('Failed Request')

    return 1