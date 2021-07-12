import boto3
from datetime import datetime

sqs = boto3.client('sqs')
queue_url = sqs.get_queue_url(QueueName="SQSQueueForLambda")


def handler(event, context):
    date = datetime.utcnow().now().strftime("%d/%m/%Y %H:%M:%S.%f")
    response = sqs.send_message(
        QueueUrl=queue_url['QueueUrl'],
        MessageBody=date
    )
