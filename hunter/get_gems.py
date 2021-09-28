import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime, timedelta


def get_gems():
    """
    Get yesterday data
    """
    yesterday = datetime.today() - timedelta(days=1)
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket='gemhunter',
                            Key=f'{yesterday.date()}/nvt.json')
    except ClientError as e:
        two_days_ago = datetime.today() - timedelta(days=2)
        obj = s3.get_object(Bucket='gemhunter',
                            Key=f'{two_days_ago.date()}/nvt.json')
    j = json.loads(obj['Body'].read().decode('utf-8'))
    return j