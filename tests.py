from __future__ import unicode_literals

import unittest
from notmuch_sync import main, merge, Dump
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


class TestMerge(unittest.TestCase):

    def _test_merge(self, ancestor, left, right, result):
        ancestor = Dump(ancestor)
        left = Dump(left)
        right = Dump(right)
        result = Dump(result)

        self.assertEqual(merge(ancestor, left, right), result)
        self.assertEqual(merge(ancestor, right, left), result)

    def _test_one(self, old, new, result):
        self._test_merge(old, old, new, result)

    def _test_both(self, old, new, result):
        self._test_merge(old, new, new, result)

    def test_all_empty(self):
        self._test_merge({}, {}, {}, {})

    def test_add(self):
        new = {'a': {'b', 'c', 'd'}}
        self._test_one({}, new, new)
        self._test_both({}, new, new)

    def test_del(self):
        old = {'a': {'b', 'c', 'd'}}
        self._test_one(old, {}, {'a': set()})
        self._test_both(old, {}, {'a': set()})

    def test_add_bothsides(self):
        self._test_merge(
            {'a': {'1', '2'}},
            {'a': {'1', '2'}, 'b': {'3'}},
            {'a': {'1', '2', '7'}},
            {'a': {'1', '2', '7'}, 'b': {'3'}},
        )
