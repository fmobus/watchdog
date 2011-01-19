#!/usr/bin/python
# vim: set fileencoding=utf-8

from __future__ import with_statement;
import time;
import unittest;

from watchdog import watchdog, Timeout;

@watchdog(3)
def dummy_sleep(delay):
	time.sleep(delay);

class TestWatchdogAsDecorator(unittest.TestCase):
	def test_raises(self):
		self.assertRaises(Timeout, dummy_sleep, 5);

	def test_does_not_raise(self):
		try:
			dummy_sleep(2);
		except Timeout, e:
			self.fail("dummy_sleep(2) timed-out under a 3 second watchdog");

class TestWatchdogAsContextManager(unittest.TestCase):
	def test_watchdog_context_raises(self):
		try:
			with watchdog(3):
				time.sleep(4)
		except Timeout, e:
			pass;
		else:
			self.fail("sleep(4) should have raised under a 3 second watchdog");

	def test_watchdog_context_does_not_raise(self):
		try:
			with watchdog(3):
				time.sleep(2);
		except Timeout, e:
			self.fail("sleep(2) shoud not raise under a 3 second watchdog");
		else:
			pass;


if __name__ == '__main__':
	unittest.main();
