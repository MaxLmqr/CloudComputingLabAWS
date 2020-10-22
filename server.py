import boto3
import time

# Get the service resource
sqs = boto3.resource('sqs', region_name='us-east-1')


def average(L):
    return sum(L)/len(L)

def median(L):
    L.sort()
    return L[len(L)//2]


# Create the queue. This returns an SQS.Queue instance
# responseQueue = sqs.create_queue(QueueName='responseQueue', Attributes={'DelaySeconds': '5'})


# Get the queue. This returns an SQS.Queue instance
requestQueue = sqs.get_queue_by_name(QueueName='requestQueue')
print('request Queue loaded.\n')
responseQueue = sqs.get_queue_by_name(QueueName='responseQueue')
print('response Queue loaded.\n')

# Loop over messages
while True:
    rq = requestQueue.receive_messages(
        MessageAttributeNames=['All'], WaitTimeSeconds=15)
    if len(rq) != 0:
        messageBody = rq[0].body
        p_mess = messageBody.split(' ')
        p_mess.pop()
        p_mess = [int(x) for x in p_mess]
        rq[0].delete()
        mean = average(p_mess)
        minimum = min(p_mess)
        maximum = max(p_mess)
        mean_response = {
            'Id': '1',
            'MessageBody': 'Moyenne : ' + str(mean),
        }
        min_response = {
            'Id': '2',
            'MessageBody': 'Minimum : ' + str(minimum),
        }
        max_response = {
            'Id': '3',
            'MessageBody': 'Maximum : ' + str(maximum),
        }
        median_response = {
            'Id': '4',
            'MessageBody': 'Median : ' + str(maximum),
        }
        responseQueue.send_messages(Entries=[mean_response])
        responseQueue.send_messages(Entries=[min_response])
        responseQueue.send_messages(Entries=[max_response])
        print('Responded.')
    else:
        print("No request yet.")

