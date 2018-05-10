'''Publish AWS health events to SNS'''

import json
import logging
import os

import boto3

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
_logger = logging.getLogger(__name__)

AWS_SNS_TOPIC_ARN = os.environ.get('AWS_SNS_TOPIC_ARN')
sns_client = boto3.client('sns')

def _create_event_data_field(k: str, v: str, short=True):
    '''Return an event data field based on a key value pair'''
    field = {
        "title": k,
        "value": v,
        "short": short
    }
    return field


def _format_slack_message(event: dict) -> dict:
    '''Return a slack message for publishing'''
    msg = {}
    msg['text'] = "AWS Health Event Notification"
    msg['attachment'] = []

    event_data = {
        "title": event.get('detail-type'),
        "author": "Amazon Web Services",
    }
    event_data_fields = []
    event_data_fields.append(
        _create_event_data_field('Type', event.get('detail-type'))
    )

    event_data_fields.append(
        _create_event_data_field('Source', event.get('source'))
    )

    event_data_fields.append(
        _create_event_data_field('Account', event.get('account'))
    )

    event_data_fields.append(
        _create_event_data_field('Service', event.get('detail').get('service'))
    )


    event_data_fields.append(
        _create_event_data_field('Event Type Code',
                                 event.get('detail').get('eventTypeCode'))
    )

    event_data_fields.append(
        _create_event_data_field('Event Type Category',
                                 event.get('detail').get('eventTypeCategory'))
    )

    event_data_fields.append(
        _create_event_data_field('Event ARN', event.get('detail').get('eventArn'))
    )


    if event.get('resources'):
        event_data_fields.append(
            _create_event_data_field('Resources', ','.join(event.get('resources')))
        )

    event_data['fields'] = event_data_fields
    msg['attachment'].append(event_data)


    for description in event.get('detail').get('eventDescription'):
        event_description = {
            'title': 'Description',
            'text': description.get('latestDescription')
        }
        msg['attachment'].append(event_description)

    return msg



def _publish_sns_message(sns_topic_arn: str, message: dict) -> None:
    '''Publish message to SNS topic'''
    r = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps(message)
    )

    return r


def handler(event, context):
    '''Function entry'''
    _logger.debug('Event received: {}'.format(json.dumps(event)))

    sns_message = _format_slack_message(event)
    _publish_sns_message(AWS_SNS_TOPIC_ARN, sns_message)

    resp = {'Status': 'OK'}
    _logger.debug('Response: {}'.format(json.dumps(resp)))
    return resp

