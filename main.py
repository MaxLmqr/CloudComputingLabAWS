import boto3

# Get the service resource
sqs = boto3.resource('sqs')


# Create the queue. This returns an SQS.Queue instance
# queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName='test')

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))

# Print out each queue name, which is part of its ARN
for queue in sqs.queues.all():
    print(queue.url)

# Create a new message
response = queue.send_message(MessageBody='world')

print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))

response = queue.send_messages(Entries=[
    {
        'Id': '1',
        'MessageBody': '12345'
    },
    {
        'Id': '2',
        'MessageBody': 'boto3',
        'MessageAttributes': {
            'Author': {
                'StringValue': 'Daniel',
                'DataType': 'String'
            }
        }
    }
])

# Print out any failures
print(response.get('Failed'))


# Process messages by printing out body and optional author name
for message in queue.receive_messages(MessageAttributeNames=['All'], MaxNumberOfMessages=5):
    # Get the custom author message attribute if it was set
    author_text = ''
    if message.message_attributes is not None:
        author_name = message.message_attributes.get(
            'Author').get('StringValue')
        if author_name:
            author_text = ' ({0})'.format(author_name)

    # Print out the body and author (if set)
    print('Hello, {0}!{1}'.format(message.body, author_text))

    # Let the queue know that the message is processed
    message.delete()

queue.delete()
