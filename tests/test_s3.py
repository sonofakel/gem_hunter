import boto3
from moto import mock_s3
from hunter.get_gems import get_gems
from datetime import datetime, timedelta
import json


def test_get_yesterday_from_s3():
    with mock_s3():
        yesterday = datetime.today() - timedelta(days=1)
        client = boto3.client('s3', region_name="us-east-1")
        client.create_bucket(Bucket='gemhunter')
        client.put_object(Bucket='gemhunter',
                          Key=f'{yesterday.date()}/nvt.json',
                          Body=json.dumps({'name': 'bitcoin'}))
        result = get_gems()
        assert result['name'] == 'bitcoin'


def test_get_two_days_ago_if_yesterday_is_missing_from_s3_and_exception_is_thrown():
    with mock_s3():
        two_days_ago = datetime.today() - timedelta(days=2)
        client = boto3.client('s3', region_name="us-east-1")
        client.create_bucket(Bucket='gemhunter')
        client.put_object(Bucket='gemhunter',
                          Key=f'{two_days_ago.date()}/nvt.json',
                          Body=json.dumps({'name': 'eth'}))
        result = get_gems()
        assert result['name'] == 'eth'
