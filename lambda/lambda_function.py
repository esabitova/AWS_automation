import boto3
from datetime import datetime
import json


# def send_message():
sqs = boto3.client('sqs')
queue_url = sqs.get_queue_url(QueueName="ff979bcd-c9c9-4ca8-9c63-0341b190876d")
# print("sqsURL" + str(queue_url))
date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# TODO: delete json format for message
message = {"date": date}
response = sqs.send_message(
    QueueUrl=queue_url['QueueUrl'],
    MessageBody=json.dumps(message)
)
print(message)


def handler(event, context):
    return {
        'body': event
    }

