:Release: 2.1
:Date: 2018-08-01

Summary -- Release highlights
=============================

* This release mostly includes fixes for bugs found after the launch of 2.0.

New checkers
============

* A new check was added, ``misplaced-format-function``.

  This message is emitted when pylint detects that a format function is called on non str object.
  This can occur due to wrong placement of closing bracket, e.g

  .. code-block:: python

    print('value: {}').format(123) # bad

    print('value: {}'.format(123)) # good


Other Changes
=============

* ``try-except-raise`` check was demoted from an error to a warning, as part of issue #2323.

* Correctly handle the new name of the Python implementation of the ``abc`` module.

  In Python 3.7, the ``abc`` module has both a C implementation as well as a Python one,
  but the Python implementation has a different file name that what ``pylint`` was expecting,
  resulting in some checks getting confused.

* Modules with ``__getattr__`` are exempted by default from ``no-member``

  There's no easy way to figure out if a module has a particular member when
  the said module uses ``__getattr__``, which is a new addition to Python 3.7.
  Instead we assume the safe thing to do, in the same way we do for classes,
  and skip those modules from checking.


* ``invalid name`` is no longer triggered for function and attribute names longer
  than 30 characters. The upper limit was removed completely.


* Fix false-positive ``undefined-variable`` for self referential class name in lamdbas

* ``no-else-return`` also specifies the type of the branch that is causing the error.

* Fixed inconsistent behaviour for bad-continuation on first line of file.

* Fixed a bug where ``pylint`` was not able to disable certain messages on the last line through
  the global disable option.

* ``pylint`` no longer emits ``useless-return`` when it finds a single statement that is the ``return`` itself

  We still want to be explicit when a function is supposed to return
  an optional value; even though ``pass`` could still work, it's not explicit
  enough and the function might look like it's missing an implementation.

* Fixed a bug where ``pylint`` was crashing when being unable to infer the value of an argument to ``next()``


* ``pylint`` no longer emit ``not-an-iterable`` when dealing with async iterators.

* ``pylint`` gained the ability to specify a default docstring type for when the check cannot guess the type

  For this we added a ``--default-docstring-type`` command line option.
