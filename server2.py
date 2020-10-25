from PIL import Image
import boto3
import time

# Get the service resource
sqs = boto3.resource('sqs', region_name='us-east-1')
s3 = boto3.client('s3')

# Get the queue. This returns an SQS.Queue instance
requestQueue = sqs.get_queue_by_name(QueueName='requestQueue')
print('request Queue loaded.\n')
responseQueue = sqs.get_queue_by_name(QueueName='responseQueue')
print('response Queue loaded.\n')


def processImage(KEY):

    BUCKET_NAME = 'mybucket974'  # replace with your bucket name
    thresh = 100

    try:
        s3.download_file(BUCKET_NAME, KEY, 'my_local_image.jpg')
    except:
        print("Problem downloading the file.")

    def fn(x): return 255 if x > thresh else 0

    img = Image.open('my_local_image.jpg')
    r = img.convert('L').point(fn, mode='1')
    r.save('processed_image.jpg')


# Loop over messages
while True:
    rq = requestQueue.receive_messages(
        MessageAttributeNames=['All'], WaitTimeSeconds=15)
    if len(rq) != 0:
        k = rq[0].body
        rq[0].delete()
        processImage(k)
        filename = 'processed_image.jpg'
        with open(filename, "rb") as f:
            s3.upload_fileobj(f, "mybucket974", "processed/myimage.jpg")
        new_k = 'processed/myimage.jpg'
        print('Processed File uploaded')
        response = {
            'Id': '1',
            'MessageBody': new_k,
        }
        responseQueue.send_messages(Entries=[response])
        print('Responded.')
    else:
        print("No request yet.")
