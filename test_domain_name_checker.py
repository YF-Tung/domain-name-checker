#!/usr/bin/env python

import unittest
from mock import patch
import domain_name_checker


class test_domain_name_checker(unittest.TestCase):

    def test_a(self):
        self.assertEqual(1, 1)

    def test_sample_func(self):
        self.assertEqual(domain_name_checker.sample_func(), 0)

    @patch('domain_name_checker.smtplib.SMTP')
    def test_send_email(self, mock_smtp):
            domain_name_checker._send_email([], [], {}, True)
            instance = mock_smtp.return_value
            self.assertTrue(instance.sendmail.called)
