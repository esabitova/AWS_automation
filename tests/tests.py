import unittest
from unittest.mock import MagicMock

import main


class MyTestCase(unittest.TestCase):

    def test_createCfn(self):
        mock_client = main.cfn_client
        mock_client.create_stack = MagicMock()

        text = 'text from template'
        main.createCfn(text)

        mock_client.create_stack.assert_called()

        # check arguments without values = all needed arguments was included.
        expected_args = ['StackName', 'TemplateBody', 'Capabilities']
        actual_args = mock_client.create_stack.call_args[1]
        list_args = []
        for i in actual_args:
            list_args.append(i)

        self.assertEqual(list_args, expected_args)

        # check values for some arguments = values correct
        actual_StackName = mock_client.create_stack.call_args[1]['StackName']
        expected_StackName = 'AWS-challenge-task'

        actual_Capabilities = mock_client.create_stack.call_args[1]['Capabilities']
        expected_Capabilities = ['CAPABILITY_AUTO_EXPAND', 'CAPABILITY_IAM']

        self.assertEqual(actual_StackName, expected_StackName)
        self.assertEqual(actual_Capabilities, expected_Capabilities)

    def test_invokeLambda(self):
        mock_client = main.lambda_client
        mock_client.invoke = MagicMock()

        main.invokeLambda(10)

        # check how many times lambda was invoked
        actual_count_calls = mock_client.invoke.call_count
        expected_calls = 10
        self.assertEqual(actual_count_calls, expected_calls)

        # check arguments without values = all needed arguments was included.
        expected_args = ['FunctionName', 'InvocationType']
        actual_args = mock_client.invoke.call_args[1]
        list_args = []
        for i in actual_args:
            list_args.append(i)

        self.assertEqual(list_args, expected_args)

        # check values arguments = values correct
        actual_FunctionName = mock_client.invoke.call_args[1]['FunctionName']
        expected_FunctionName = 'SendMessagesLambda'

        actual_InvocationType = mock_client.invoke.call_args[1]['InvocationType']
        expected_InvocationType = 'Event'

        self.assertEqual(actual_FunctionName, expected_FunctionName)
        self.assertEqual(actual_InvocationType, expected_InvocationType)

    def test_cloudWatch(self):
        # cloud_watch client
        mock_client = main.cw_client
        mock_client.get_metric_statistics = MagicMock(
            return_value={'Label': 'NumberOfMessagesSent', 'Datapoints': [{'Sum': 10.0, 'Unit': 'Count'}],
                          'ResponseMetadata': {'RequestId': 'd764cfec-e8d0-4f0a-ab18-77e4fb95ef8c',
                                               'HTTPStatusCode': 200, 'RetryAttempts': 0}}
        )

        main.cloudWatch()

        mock_client.get_metric_statistics.assert_called()

        # check arguments without values = all needed arguments was included.
        expected_args = ['Namespace', 'MetricName', 'Dimensions', 'StartTime', 'EndTime', 'Period', 'Statistics',
                         'Unit']
        actual_args = mock_client.get_metric_statistics.call_args[1]
        list_args = []
        for i in actual_args:
            list_args.append(i)

        self.assertEqual(list_args, expected_args)

        # check values for some arguments = values correct
        actual_MetricName = mock_client.get_metric_statistics.call_args[1]['MetricName']
        expected_MetricName = 'NumberOfMessagesSent'

        actual_Namespace = mock_client.get_metric_statistics.call_args[1]['Namespace']
        expected_Namespace = 'AWS/SQS'

        actual_Dimensions = mock_client.get_metric_statistics.call_args[1]['Dimensions']
        expected_Dimensions = [{'Name': 'QueueName', 'Value': 'SQSQueueForLambda'}]

        self.assertEqual(actual_MetricName, expected_MetricName)
        self.assertEqual(actual_Namespace, expected_Namespace)
        self.assertEqual(actual_Dimensions, expected_Dimensions)

        # check return value
        result = main.cloudWatch()
        self.assertEqual(result, 10)
