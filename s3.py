import boto3
import logging
import io

s3 = boto3.client("s3")

log = logging.getLogger("some_log_name")
log.info("Hello S3")

log = logging.getLogger("some_log_name")
log_stringio = io.StringIO()
handler = logging.StreamHandler(log_stringio)
log.addHandler(handler)


s3.put_object(Body=log_stringio.getvalue(), Bucket="mybucket974", Key="mykey")
