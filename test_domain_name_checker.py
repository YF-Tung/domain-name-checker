#!/usr/bin/env python

import unittest
import domain_name_checker


class test_domain_name_checker(unittest.TestCase):

    def test_a(self):
        self.assertEqual(1, 1)

    def test_sample_func(self):
        self.assertEqual(domain_name_checker.sample_func(), 0)


if __name__ == '__main__':
    unittest.main()
