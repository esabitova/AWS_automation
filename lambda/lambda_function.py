import boto3
from datetime import datetime

sqs = boto3.client('sqs')
queue_url = sqs.get_queue_url(QueueName="SQSQueueForLambda")
date = datetime.utcnow().now().strftime("%d/%m/%Y %H:%M:%S.%f")


def handler(event, context):
    response = sqs.send_message(
        QueueUrl=queue_url['QueueUrl'],
        MessageBody=date
    )
