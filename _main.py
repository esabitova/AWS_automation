import boto3
from cfn_tools import load_yaml, dump_yaml

text = open('./sqs/cf_template.yml').read()
data = load_yaml(text)

print(dump_yaml(data))

client = boto3.client('cloudformation')
response = client.create_stack(
    StackName='AWS-challenge-task34',
    TemplateBody=dump_yaml(data),
    Capabilities=[
        'CAPABILITY_AUTO_EXPAND','CAPABILITY_IAM'
    ]
)


#
#
# # Press the green button in the gutter to run the script.
def createCfn():
    pass


if __name__ == '__main__':
    createCfn()
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
