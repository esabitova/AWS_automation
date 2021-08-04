import time
from datetime import datetime, timedelta

import boto3
from cfn_tools import load_yaml, dump_yaml


STACK_NAME = 'AWS-challenge-task2'
FUNCTION_NAME = 'SendMessagesLambda'
TEMPLATE_FILE = './cfn/packaged-template.yml'


cfn_client = boto3.client('cloudformation')
lambda_client = boto3.client('lambda')
cw_client = boto3.client('cloudwatch')


def textLoader():
    text = open(TEMPLATE_FILE).read()
    data = load_yaml(text)
    strText = dump_yaml(data)
    return strText


def createCfn(text):
    response = cfn_client.create_stack(
        StackName=STACK_NAME,
        TemplateBody=text,
        Capabilities=[
            'CAPABILITY_AUTO_EXPAND', 'CAPABILITY_IAM'
        ]
    )
    print(response)


def waitCfn():
    waiter = cfn_client.get_waiter('stack_create_complete')
    waiter.wait(
        StackName=STACK_NAME
    )


def invokeLambda(num):
    for x in range(0, num):
        response = lambda_client.invoke(
            FunctionName= FUNCTION_NAME,
            InvocationType='Event',
        )


def cloudWatch():
    count = 0
    currentDate = datetime.utcnow()
    response = cw_client.get_metric_statistics(
        Namespace='AWS/SQS',
        MetricName='NumberOfMessagesSent',
        Dimensions=[
            {'Name': 'QueueName', 'Value': 'SQSQueueForLambda'}
        ],
        StartTime=currentDate - timedelta(minutes=5),
        EndTime=currentDate,
        Period=300,
        Statistics=['Sum'],
        Unit='Count'
    )

    for i in response['Datapoints']:
        count = (i['Sum'])

    return count


if __name__ == '__main__':
    templateText = textLoader()
    createCfn(templateText)
    waitCfn()
    invokeLambda(10)
    time.sleep(180)
    cloudWatch()
