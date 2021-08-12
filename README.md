# AWS_Automation
Project for automation AWS services: CloudFormation, Lambda, SQS, CloudWatch.
Creates CloudFormation by the Template, where it creates SQS Standard Queue, Lambda Function and Lambda Role.
Lambda Function sends messages to SQS with the current date and time.
Then CloudWatch receives metric statistics with the number of messages in SQS.

Prerequisites:
1. Python 3.8
2. Make
3. S3 bucket with name "bucketfortemplate".
If you already have the bucket with a different name, you should change BUCKET_NAME in the Makefile


### Execution command
```
make execute
```
The project has been debugged on Windows 10.
Project launch on other OS may differ.
