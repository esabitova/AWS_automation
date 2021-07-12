from datetime import datetime, timedelta

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


def invokeLambda():
    client = boto3.client('lambda')

    for x in range(0, 10):
        response = client.invoke(
            FunctionName='SendMessagesLambda',
            InvocationType='Event',
            Payload='{}'
        )
        print(response)


def cloudWatch():
    client = boto3.client('cloudwatch')
    count = 0
    response = client.get_metric_statistics(
        Namespace='AWS/SQS',
        MetricName='NumberOfMessagesSent',
        Dimensions=[
            {'Name': 'QueueName', 'Value': 'SQSQueueForLambda'}
        ],
        StartTime=datetime.now() - timedelta(hours=3),
        EndTime=datetime.now(),
        Period=60,
        Statistics=['Sum'],
        Unit='Count'
    )

    for i in response['Datapoints']:
        count = (i['Sum'])

    return count


if __name__ == '__main__':
    createCfn()
    # invokeLambda()
    # cloudWatch()
