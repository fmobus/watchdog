License
=======
This code is licensed under the MIT license
This code is based on a implementation by Nick Garvish, found on http://nick.vargish.org/clues/python-tricks.html


Simple Signal Watchdog
----------------------

Provides a simple UNIX-signal based watchdog. It may be used either as a context manager
or as a decorator. The default behaviour is to raise a Timeout exception when the
given number of seconds has passed.

Usage
=====

Decorator usage
---------------

	>>> @watchdog(3)
	>>> def nii(delay):
	...   time.sleep(delay);
	...

	>>> nii(2);          # will pass successfully
	>>> nii(3);          # will pass successfully
	>>> nii(4);
	[...]
	watchdog.Timeout: Execution timed out (limit was 3 seconds)

Context Manager usage
---------------------
	>>> with watchdog(5):
	...   time.sleep(10);
	watchdog.Timeout: Execution timed out (limit was 5 seconds)

Remarks
=======

Portability
-----------

This implementation is based on UNIX signals and, as such, should not work on non-
unix platforms (e.g. Windows).

Advantages
----------

This implementation is simpler than using threads. Also, unlike a thread-based
implementation, it manages to raise an exception in the same context as the calling
code.

Disavantadges
-------------
It is less capable than a thread-based watchdog implementation, in that its timeout
granularity is seconds.

Also, some people reported that it may not work under certain unknown conditions.
I have not seen it happen so far. This is discussed by Gavin Andressen in detail on
http://gavintech.blogspot.com/2008/02/python-sigalrm-oddness.html (where another
implementation (fork-based) implementation is suggested).
