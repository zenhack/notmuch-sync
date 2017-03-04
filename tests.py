from __future__ import unicode_literals

import unittest
from notmuch_sync import main
from io import StringIO


class MockExit(Exception):

    def __init__(self, status):
        Exception.__init__(self)
        self.status = status


class PassNow(Exception):
    pass


class DontUse(object):

    def __init__(self, name, testcase):
        self.__name = name
        self.__testcase = testcase

    def __getattribute__(self, name):
        self.__testcase.fail('Tried to read attribute %r of object %r.',
                             name, self.__name)

    def __setattribute__(self, name, value):
        self.__testcase.fail('Tried to set attribute %r of object %r to %r.',
                             name, self.__name, value)


class TestUsage(unittest.TestCase):

    def _assert_exit(self, status, f):
        def _exit(n):
            raise MockExit(n)
        try:
            f(exit=_exit)
            self.fail('function did not call exit')
        except MockExit as e:
            self.assertEqual(e.status, status)

    def _assert_wrong_args(self, argv):
        stderr = StringIO()
        self._assert_exit(
            1,
            lambda exit: main(
                argv=argv,
                exit=exit,
                stderr=stderr,
                open=DontUse('open', self)
            ))
        self.assertEqual(
            stderr.getvalue(),
            "usage: main <ancestor> <left> <right> <result>\n",
        )

    def test_no_args(self):
        self._assert_wrong_args(['main'])

    def test_too_few(self):
        self._assert_wrong_args(['main', '1', '2', '3'])

    def test_too_many_args(self):
        self._assert_wrong_args(['main', '1', '2', '3', '4', '5'])

    def test_args_ok(self):

        def _open_pass(name, mode='r'):
            raise PassNow()

        try:
            main(
                argv=['main', '1', '2', '3', '4'],
                exit=DontUse('exit', self),
                stderr=DontUse('stderr', self),
                open=_open_pass,
            )
            self.fail("main didn't call open.")
        except PassNow:
            pass
