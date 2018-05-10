# aws-health-event-publisher
[![Serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

Publish an AWS Health event to an SNS topic.

![System Architecture](/diagram.png?raw=true "System Architecture")

## Outputs

* __aws-health-event-publisher-${stage}-HealthEventSnsTopicArn__: AWS SNS topic ARN where healthe vents are published to.
