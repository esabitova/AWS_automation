import unittest
from unittest.mock import MagicMock

import _main


class MyTestCase(unittest.TestCase):

    def test_createCfn(self):
        mock_client = _main.cfn_client
        mock_client.create_stack = MagicMock()

        _main.createCfn()

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

        #     TODO: check the response

    def test_invokeLambda(self):
        mock_client = _main.lambda_client
        mock_client.invoke = MagicMock()

        _main.invokeLambda()

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

    #   TODO: check the response

    def test_cloudWatch(self):
        # cloud_watch client
        mock_client = _main.cw_client
        mock_client.get_metric_statistics = MagicMock()

        # call the method
        _main.cloudWatch()

        # check, that client was called
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

        print(mock_client.get_metric_statistics.call_args)

        #   TODO: check the response - count?
        response = 10
        mock_client.get_metric_statistics = MagicMock(return_value=response)
        self.assertEqual(mock_client.get_metric_statistics.return_value, response)
