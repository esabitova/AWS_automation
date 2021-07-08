import boto3
from cfn_tools import load_yaml, dump_yaml

text = open('./cfn/template.yml').read()
data = load_yaml(text)
# TODO: clean
print(dump_yaml(data))


def createCfn():
    client = boto3.client('cloudformation')
    response = client.create_stack(
        StackName='AWS-challenge-task34',
        TemplateBody=dump_yaml(data),
        Capabilities=[
            'CAPABILITY_AUTO_EXPAND', 'CAPABILITY_IAM'
        ]
    )


# def sendMessage():



if __name__ == '__main__':
    createCfn()
