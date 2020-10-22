import boto3

s3 = boto3.client("s3")


s3.put_object(Body="Hello s3", Bucket='mybucket974',
              Key='mykey/anotherfilename.txt')
