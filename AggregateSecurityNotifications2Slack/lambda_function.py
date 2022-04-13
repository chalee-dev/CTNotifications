import json, boto3,requests

def lambda_handler(event, context): 
    
    # Sample Code Reference : https://dev.to/aws-builders/send-aws-config-notification-to-slack-1f7j
    # How to use requests module in AWS Lambda : https://www.gcptutorials.com/article/how-to-use-requests-module-in-aws-lambda

    webhook_url = "Change me"
    
    #SNS Code
    
    eventMsg = event['Records'][0]['Sns']['Message']
    ctMsg = json.loads(eventMsg)
    
    print("===================== ctMsg  Msg ===================== ")
    print(ctMsg)
    etime = ctMsg["time"]
    region = ctMsg["region"]
    rule = ctMsg["detail"]["configRuleName"]
   
    resource_type = ctMsg["detail"]["newEvaluationResult"]["evaluationResultIdentifier"]["evaluationResultQualifier"]["resourceType"]
    resource_id = ctMsg["detail"]["newEvaluationResult"]["evaluationResultIdentifier"]["evaluationResultQualifier"]["resourceId"]
    compliance = ctMsg["detail"]["newEvaluationResult"]["complianceType"]
    

    slack_data = slack_data = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n*Config Compliance Change* :alert_:"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*`Compliance:`*  " + compliance + "\n*`Time:`* " + etime + "\n*`Region:`* " + region + "\n*`Rule:`* " + rule +"\n*`Resource Type:`* "+resource_type+"\n*`Resource ID:`* "+ resource_id
            },
            "accessory": {
                "type": "image",
                "image_url": "https://i.ibb.co/BjWcWKt/Picture1.png",
                "alt_text": "thumbnail"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "For more details."
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "AWS Config"
                },
                "value": "click_me_123",
                "url": "https://console.aws.amazon.com/config/home?region="+region+"#/timeline/"+resource_type+"/"+resource_id+"/configuration",
                "action_id": "button-action"
            }
        }
    ]
}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )
    