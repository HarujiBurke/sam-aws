import os
import pathlib
import sys
import logging


def prepare_invoke():
    TARGET_DIRECTORY = pathlib.Path(
        os.path.dirname(__file__) + '/../src').resolve()
    sys.path.append(str(TARGET_DIRECTORY))
    # environment variables in docker-compose.yml
    TEST_AWS_ACCESS_KEY_ID = 'local-id'
    TEST_AWS_SECRET_ACCESS_KEY = 'local-secret'
    TEST_ENDPOINT_URL = 'http://localhost:4566'
    TEST_AWS_REGION = 'ap-northeast-1'

    os.environ['BUCKET_NAME'] = 'toki-sam-in-real-bucket'
    os.environ['OBJECT_KEY'] = 'demo-object-file.csv'
    os.environ['DEBUG_AWS_REGION'] = TEST_AWS_REGION
    os.environ['DEBUG_S3_ENDPOINT'] = TEST_ENDPOINT_URL
    os.environ['DEBUG_AWS_ACCESS_KEY_ID'] = TEST_AWS_ACCESS_KEY_ID
    os.environ['DEBUG_AWS_SECRET_ACCESS_KEY'] = TEST_AWS_SECRET_ACCESS_KEY


def invoke():
    prepare_invoke()
    from lambda_function import lambda_handler as target_lambda
    # override formatter
    # - remove 'aws_request_id'
    root_logger = logging.getLogger()
    root_logger.handlers[0].setFormatter(logging.Formatter(
        '%(asctime)s.%(msecs)dZ\t%(levelname)s\t%(message)s', '%Y-%m-%dT%H:%M:%S'
    ))
    result = target_lambda('event', 'context')
    print(result)


invoke()
