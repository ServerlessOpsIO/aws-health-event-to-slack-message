'''Test health_event_publisher'''
# pylint: disable=protected-access
# pylint: disable=wrong-import-position
# pylint: disable=redefined-outer-name
import json
import os

import boto3
import jsonschema
from moto import mock_sns, mock_sts
import pytest

import handlers.aws_health_event_publisher as h  # noqa

EVENT_FILE = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    'events',
    'aws_health_event_publisher.json'
)

SLACK_SCHEMA_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../../slack-message-schema.json'
)

SNS_TOPIC_NAME = "mock-aws-health-event-to-slack-message"

@pytest.fixture()
def event(event_file=EVENT_FILE):
    '''Trigger event'''
    with open(event_file) as f:
        return json.load(f)


@pytest.fixture()
def slack_message_schema():
    '''Slack message schema'''
    with open(SLACK_SCHEMA_FILE_PATH) as f:
        return json.load(f)


@pytest.fixture()
def sns_client():
    '''SNS client'''
    return boto3.client('sns')


@pytest.fixture()
def sns_message(event):
    '''SNS message'''
    return h._format_slack_message(event)


@pytest.fixture
def sns_topic_name():
    '''SNS topic name'''
    return SNS_TOPIC_NAME


def test__format_slack_message(event, slack_message_schema):
    '''Test format of message message to be published'''
    slack_message = h._format_slack_message(event)
    jsonschema.validate(slack_message, slack_message_schema)


@mock_sts
@mock_sns
def test__publish_sns_message(sns_client, sns_message, sns_topic_name):
    '''Test publish an SNS message.'''

    sns_create_topic_resp = sns_client.create_topic(Name=sns_topic_name)
    sns_publish_resp = h._publish_sns_message(
        sns_create_topic_resp.get('TopicArn'),
        sns_message
    )

    assert sns_publish_resp.get('ResponseMetadata').get('HTTPStatusCode') == 200

