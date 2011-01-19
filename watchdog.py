__author__ = 'Felipe Mobus <fmobus@propus.com.br>'
__version__ = '$Revision 1$'

"""
For license and instructions, please see the README file
"""


import signal;

class Timeout(Exception):
	def __init__(self, timeout):
		Exception.__init__(self, "Execution timed out (limit was %d seconds)" % timeout);

class watchdog():
	def __init__(self, timeout, handler = None):
		"""
		Expects an integer as a timeout parameter. A custom handler may be defined, and may
		raise exceptions visible to the calling code. It should be noticed that when the
		handler kicks in, the watched code execution is dead (and probably GC'd).
		"""
		assert isinstance(timeout, int);
		self.timeout     = timeout;
		self._handler    = handler or self.default_handler;
		self.old_handler = None;

	def __call__(self, func):
		"""
		This is useful in the decorator usage. When you use a decorator, python actually
		does the following:
		>>> func = mydecorator(func);

		Since a watchdog requires a decorator (given to the constructor), we actually need
		something like:

		>>> func = watchdog(timeout)(func);

		Id est, the constructor returns a callable object of the watchdog class, leaving the
		dirty injection work to the __call__ method.

		(I actually started it as a pure function... but having a function that returns a
		function that accepts another function given a function is quite disturbing :)
		"""
		def _injected(*args, **kw):
			self.old_handler = signal.signal(signal.SIGALRM, self._handler);
			signal.alarm(self.timeout);
			try:
				result = func(*args, **kw);
			finally:
				signal.signal(signal.SIGALRM, self.old_handler);
				signal.alarm(0);
			return result;
		return _injected

	def __enter__(self):
		"""
		This method adheres to the context manager protocol. It sets up the
		alarm and saves the old handler
		"""
		self.old_handler = signal.signal(signal.SIGALRM, self._handler);
		signal.alarm(self.timeout);
		return self;

	def __exit__(self, *exc_info):
		"""
		This methods adheres to the context manager protocol. It will disable
		the alarm, restore the old handler and propagate any exception raised
		inside the managed block.
		"""
		signal.signal(signal.SIGALRM, self.old_handler);
		signal.alarm(0);

	def default_handler(self, signum, handler):
		"""
		The default handler. It handles timeouts by simply raising a Timeout
		exception. This exception will be visible to the calling context.
		"""
		raise Timeout(self.timeout);

