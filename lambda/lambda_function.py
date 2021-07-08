import boto3
from datetime import datetime

sqs = boto3.client('sqs')
# TODO: hardcoded? think how to get QueueName variable without hardcoding
queue_url = sqs.get_queue_url(QueueName="SQSQueueForLambda")
# TODO: clean
print("sqsURL" + str(queue_url))

date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

response = sqs.send_message(
    QueueUrl=queue_url['QueueUrl'],
    MessageBody=date
)
# TODO: clean
print(date)


def handler(event, context):
    return {
        'body': event
    }
