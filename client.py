import boto3
import time

# Service resource
sqs = boto3.resource('sqs')

# Create queue named : requestQueue
# queue = sqs.create_queue(QueueName='requestQueue',
#                          Attributes={'DelaySeconds': '5'})


# Get the queue. This returns an SQS.Queue instance
requestQueue = sqs.get_queue_by_name(QueueName='requestQueue')
print('request Queue loaded.\n')
responseQueue = sqs.get_queue_by_name(QueueName='responseQueue')
print('response Queue loaded.\n')


# Load the content of the input.
with open('input.txt') as f:
    inputFile = f.readlines()
inputFile = [x.strip() for x in inputFile]
inputStr = ''
for x in inputFile:
    inputStr += str(x)+' '

print('File loaded.\n')

# Generate the message to send
message = {
    'Id': '1',
    'MessageBody': inputStr
}
requestQueue.send_messages(Entries=[message])
print('Message sent.\n')
# Message sent

# Getting ready to receive a response.
# Loop over messages
while True:
    resp = responseQueue.receive_messages(
        MessageAttributeNames=['All'], WaitTimeSeconds=15)
    if len(resp) != 0:
        print(resp[0].body)
        resp[0].delete()
    else:
        print('No answers received from the server')
        break
