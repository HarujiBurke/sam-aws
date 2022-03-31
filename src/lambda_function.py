from util.s3_util import S3Util

import logging
import os
import json

logging.basicConfig()
logger = logging.getLogger()
logger.handlers[0].setFormatter(
    logging.Formatter('%(asctime)s.%(msecs)dZ\t[%(aws_request_id)s]\t%(levelname)s\t%(message)s', '%Y-%m-%dT%H:%M:%S'))
logger.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))

common = {
    'BUCKET_FILE': os.environ['BUCKET_NAME'],
    'NAME_FILE': os.environ['OBJECT_KEY'],
}

s3_util = S3Util(
    logger,
    aws_access_key_id=os.environ.get('DEBUG_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('DEBUG_AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('DEBUG_AWS_REGION'),
    endpoint_url=os.environ.get('DEBUG_S3_ENDPOINT')
)


def lambda_handler(event, context):
    print("lambda is starting")
    content = prepare_content()
    write_file(content)
    return {
        'statusCode': 200,
        'body': json.dumps('Done!!')
    }


def prepare_content():
    result = 'id,name\nid-stack,hello-sam-in-real\n'
    return result


def write_file(content):
    writing_result = s3_util.write_file(
        common['BUCKET_FILE'], common['NAME_FILE'], content, 'utf-8')
    if writing_result['status'] == 500:
        logger.warning("ERROR_WHILE_WRITING_LOG")
