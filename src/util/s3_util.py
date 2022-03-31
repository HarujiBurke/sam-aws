from asyncio.log import logger
import boto3
from botocore.exceptions import ClientError


class S3Util:
    def __init__(self, logger, aws_access_key_id=None,
                 aws_secret_access_key=None, endpoint_url=None, region_name=None):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               endpoint_url=endpoint_url,
                               region_name=region_name)
        self.logger = logger

    def write_file(self, bucket_name, file_name, content, encoding='utf-8'):
        self.logger.info("writing s3: " + bucket_name + "/" + file_name)
        result = self.s3.put_object(
            Bucket=bucket_name, Key=file_name, Body=content, ContentEncoding=encoding)
        res = result.get('ResponseMetadata')
        if res.get('HTTPStatusCode') != 200:
            self.logger.warning("error while writing s3: " +
                                bucket_name + "/" + file_name)
            return {
                'status': 500,
                'content': "error while writing s3: " + bucket_name + "/" + file_name
            }
        self.logger.info("wrote successfully: " +
                         bucket_name + "/" + file_name)
        return {
            'status': 200,
            'content': "wrote successfully"
        }
