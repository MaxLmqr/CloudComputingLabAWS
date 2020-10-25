import boto3
import time

# Service resource
sqs = boto3.resource('sqs')
s3 = boto3.client('s3')

# Create queue named : requestQueue
# queue = sqs.create_queue(QueueName='requestQueue',
#                          Attributes={'DelaySeconds': '5'})


# Get the queue. This returns an SQS.Queue instance
requestQueue = sqs.get_queue_by_name(QueueName='requestQueue')
print('request Queue loaded.\n')
responseQueue = sqs.get_queue_by_name(QueueName='responseQueue')
print('response Queue loaded.\n')

filename = 'image.jpg'
with open(filename, "rb") as f:
    uplog = s3.upload_fileobj(f, "mybucket974", "original/myimage.jpg")
print('File uploaded')
key = "original/myimage.jpg"

# Generate the message to send
message = {
    'Id': '1',
    'MessageBody': key
}
requestQueue.send_messages(Entries=[message])
print('Message sent.\n')
# Message sent

# Getting ready to receive a response.
# Loop over messages
while True:
    resp = responseQueue.receive_messages(
        MessageAttributeNames=['All'], WaitTimeSeconds=20)
    if len(resp) != 0:
        new_key = resp[0].body
        resp[0].delete()
        BUCKET_NAME = 'mybucket974'  # replace with your bucket name
        s3.download_file(BUCKET_NAME, new_key, 'output_image.jpg')
        print('File downloaded.')
        break
    else:
        print('No answers received from the server')
