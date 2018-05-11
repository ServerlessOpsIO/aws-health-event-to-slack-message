# aws-health-event-publisher
[![Serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

Publish an AWS Health event formatted as a Slack API _chat.postMessage_ message to an SNS topic.

![System Architecture](/diagram.png?raw=true "System Architecture")

This is intended to be used with [aws-sns-to-slack-publisher](https://github.com/ServerlessOpsIO/aws-sns-to-slack-publisher)

## Service Interface

* __Event Type:__ AWS CloudWatch Event - Health Event
* __Event Message:__ The message shape may be found here: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#health-event-types

Example event:

```json
{
  "version": "0",
  "id": "7bf73129-1428-4cd3-a780-95db273d1602",
  "detail-type": "AWS Health Event",
  "source": "aws.health",
  "account": "123456789012",
  "time": "2016-06-05T06:27:57Z",
  "region": "%%region%%",
  "resources": [],
  "detail": {
    "eventArn": "arn:aws:health:%%region%%::event/%%id%%",
    "service": "service",
    "eventTypeCode": "AWS_%%service_code%%",
    "eventTypeCategory": "%%category%%",
    "startTime": "Sun, 05 Jun 2016 05:01:10 GMT",
    "endTime": "Sun, 05 Jun 2016 05:30:57 GMT",
    "eventDescription": [{
      "language": "%%lang-code%%",
      "latestDescription": "%%description%%"
    }]
    ...
  }
}
```

## Deployment

This application is intended to be deployed using [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/).  However, [Serverless Framework](https://www.serverless.com) is also supported.

## Exports

* ${stack_name}-${stage}-HealthEventSnsTopicArn__: AWS SNS topic ARN where health events are published to.
