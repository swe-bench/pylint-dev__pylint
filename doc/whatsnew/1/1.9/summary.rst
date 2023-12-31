:Release: 1.9
:Date: 2018-05-15


Summary -- Release highlights
=============================

* None so far

New checkers
============

* A new Python 3 checker was added to warn about the removed ``operator.div`` function.

* A new Python 3 checker was added to warn about accessing functions that have been
  moved from the urllib module in corresponding subpackages, such as ``urllib.request``.

  .. code-block:: python

      from urllib import urlencode

  Instead the previous code should use ``urllib.parse`` or ``six.moves`` to import a
  module in a Python 2 and 3 compatible fashion:

  .. code-block:: python

      from six.moves.urllib.parse import urlencode


  To have this working on Python 3 as well, please use the ``six`` library:

  .. code-block:: python

      six.reraise(Exception, "value", tb)


* A new check was added to warn about using unicode raw string literals. This is
  a syntax error in Python 3:

  .. rstcheck: ignore-next-code-block
  .. code-block:: python

      a = ur'...'

* Added a new ``deprecated-sys-function`` check, emitted when accessing removed ``sys`` members.

* Added ``xreadlines-attribute`` check, emitted when the ``xreadlines()`` attribute is accessed
  on a file object.

* Added two new Python 3 porting checks, ``exception-escape`` and ``comprehension-escape``

  These two are emitted whenever pylint detects that a variable defined in the
  said blocks is used outside of the given block. On Python 3 these values are deleted.

  .. code-block:: python

      try:
        1/0
      except ZeroDivisionError as exc:
         ...
      print(exc) # This will raise a NameError on Python 3

      [i for i in some_iterator if some_condition(i)]
      print(i) # This will raise a NameError on Python 3


Other Changes
=============

* ``defaultdict`` and subclasses of ``dict`` are now handled for `dict-iter-*` checks. That
  means that the following code will now emit warnings for when ``iteritems`` and friends
  are accessed:

  .. code-block:: python

      some_dict = defaultdict(list)
      ...
      some_dict.iterkeys()

* Enum classes no longer trigger ``too-few-methods``

* Special methods now count towards ``too-few-methods``,
  and are considered part of the public API.
  They are still not counted towards the number of methods for
  ``too-many-methods``.

* docparams allows abstract methods to document returns documentation even
  if the default implementation does not return something.
  They also no longer need to document raising a NotImplementedError.
