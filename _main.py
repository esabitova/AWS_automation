import boto3
from cfn_tools import load_yaml, dump_yaml

text = open('./cfn/template.yml').read()
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


if __name__ == '__main__':
    createCfn()
    invokeLambda()
