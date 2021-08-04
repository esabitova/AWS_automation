import time
from datetime import datetime, timedelta, date

import boto3
from cfn_tools import load_yaml, dump_yaml

cfn_client = boto3.client('cloudformation')
lambda_client = boto3.client('lambda')
cw_client = boto3.client('cloudwatch')


# text = open('../packaged-template.yml').read()


def createCfn():
    text = open('../cfn/packaged-template.yml').read()
    data = load_yaml(text)

    response = cfn_client.create_stack(
        StackName='AWS-challenge-task',
        TemplateBody=dump_yaml(data),
        Capabilities=[
            'CAPABILITY_AUTO_EXPAND', 'CAPABILITY_IAM'
        ]
    )
    waiter = cfn_client.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='AWS-challenge-task'
    )


def invokeLambda():
    for x in range(0, 10):
        response = lambda_client.invoke(
            FunctionName='SendMessagesLambda',
            InvocationType='Event',
            # Payload='{}'
        )


def cloudWatch():
    count = 0
    response = cw_client.get_metric_statistics(
        Namespace='AWS/SQS',
        MetricName='NumberOfMessagesSent',
        Dimensions=[
            {'Name': 'QueueName', 'Value': 'SQSQueueForLambda'}
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=5),
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
    time.sleep(180)
    cloudWatch()
