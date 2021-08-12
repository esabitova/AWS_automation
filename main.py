from datetime import datetime, timedelta

import boto3
from cfn_tools import load_yaml, dump_yaml

cfn_client = boto3.client('cloudformation')
lambda_client = boto3.client('lambda')
cw_client = boto3.client('cloudwatch')


def textLoader(file):
    """
    Converts a template to the string
    :param file: Path to the template file
    :return: string with template body
    """
    text = open(file).read()
    data = load_yaml(text)
    strText = dump_yaml(data)
    return strText


def createCfn(text):
    """
    Creates a stack by template, where creates SQS Standard Queue, Lambda Function and Lambda Role
    :param text: converted to the string template body
    """
    response = cfn_client.create_stack(
        StackName='AWS-challenge-task',
        TemplateBody=text,
        Capabilities=[
            'CAPABILITY_IAM'
        ]
    )


def waitCfn():
    """
    Waiting for the stack creation to complete
    """
    waiter = cfn_client.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='AWS-challenge-task'
    )


def invokeLambda(num):
    """
    Invokes Lambda Function asynchronously. Lambda Function send messages with current date and time to the SQS
    :param num: number of invocations
    """
    for x in range(0, num):
        response = lambda_client.invoke(
            FunctionName='SendMessagesLambda',
            InvocationType='Event',
        )


def cloudWatch():
    """
    Gets metric statistics: how many messages in the SQS
    :return: number of messages from the SQS
    """
    metrics_result = 0
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
        metrics_result = (i['Sum'])

    return metrics_result


if __name__ == '__main__':
    templateText = textLoader('./cfn/packaged-template.yml')
    createCfn(templateText)
    waitCfn()
    invokeLambda(10)
    # To get the metric statistics with result, the App should wait for about 3 minutes.
    # Otherwise result will be 0, because CloudWatch receive data with a delay.
    # time.sleep(180)
    cloudWatch()
