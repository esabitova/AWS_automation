import time
from datetime import datetime, timedelta, date

import boto3
from cfn_tools import load_yaml, dump_yaml


text = open('./packaged-template.yml').read()
data = load_yaml(text)


def createCfn():
    client = boto3.client('cloudformation')
    response = client.create_stack(
        StackName='AWS-challenge-task',
        TemplateBody=dump_yaml(data),
        Capabilities=[
            'CAPABILITY_AUTO_EXPAND', 'CAPABILITY_IAM'
        ]
    )
    waiter = client.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='AWS-challenge-task'
    )
    print(waiter)


def invokeLambda():
    client = boto3.client('lambda')

    for x in range(0, 10):
        response = client.invoke(
            FunctionName='SendMessagesLambda',
            InvocationType='Event',
            # Payload='{}'
        )
        print(response)
    time.sleep(180)



def cloudWatch():
    client = boto3.client('cloudwatch')
    count = 0
    response = client.get_metric_statistics(
        Namespace='AWS/SQS',
        MetricName='NumberOfMessagesSent',
        Dimensions=[
            {'Name': 'QueueName', 'Value': 'SQSQueueForLambda'}
        ],
        StartTime=datetime.utcnow()-timedelta(minutes=5),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Sum'],
        Unit='Count'
    )

    for i in response['Datapoints']:
        count = (i['Sum'])
    print(count)
    return count


if __name__ == '__main__':
    # createCfn()
    invokeLambda()
    cloudWatch()

