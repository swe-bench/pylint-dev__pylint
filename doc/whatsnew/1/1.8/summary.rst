:Release: 1.8
:Date: 2017-12-15


Summary -- Release highlights
=============================

* None so far

New checkers
============

* A new check was added, ``shallow-copy-environ``.

  This warning message is emitted when shallow copy of os.environ is created.
  Shallow copy of os.environ doesn't work as people may expect. os.environ
  is not a dict object but rather a proxy object, so any changes made
  on copy may have unexpected effects on os.environ

  Instead of copy.copy(os.environ) method os.environ.copy() should be used.

  See https://bugs.python.org/issue15373 for details.

  .. code-block:: python

     import copy
     import os
     wrong_env_copy = copy.copy(os.environ)  # will emit pylint warning
     wrong_env_copy['ENV_VAR'] = 'new_value'  # changes os.environ
     assert os.environ['ENV_VAR'] == 'new_value'

     good_env_copy = dict(os.environ)  # the right way
     good_env_copy['ENV_VAR'] = 'different_value'  # doesn't change os.environ
     assert os.environ['ENV_VAR'] == 'new_value'

* A new check was added, ``keyword-arg-before-vararg``.

  This warning message is emitted when a function is defined with a keyword
  argument appearing before variable-length positional arguments (\*args).
  This may lead to args list getting modified if keyword argument's value is
  not provided in the function call assuming it will take default value provided
  in the definition.

  .. rstcheck: ignore-next-code-block
  .. code-block:: python

     def foo(a, b=3, *args):
         print(a, b, args)

     # Case1: a=0, b=2, args=(4,5)
     foo(0,2,4,5) # 0 2 (4,5) ==> Observed values are same as expected values

     # Case2: a=0, b=<default_value>, args=(4,5)
     foo(0,4,5) # 0 4 (5,) ==> args list got modified as well as the observed value of b

     # Case3: Syntax Error if tried as follows
     foo(0,b=2,4,5) # syntax error

* A new check was added, ``simplify-boolean-expression``.

  This message is emitted when ``consider-using-ternary`` check would emit
  not equivalent code, due to truthy element being falsy in boolean context.

  .. code-block:: python

     value = condition and False or other_value

  This flawed construct may be simplified to:

  .. code-block:: python

     value = other_value

* A new check was added, ``bad-thread-instantiation``.

  This message is emitted when the threading.Thread class does not
  receive the target argument, but receives just one argument, which
  is by default the group parameter.

  In the following example, the instantiation will fail, which is definitely
  not desired:

  .. code-block:: python

     import threading
     threading.Thread(lambda: print(1)) # Oups, this is the group parameter

* A new Python 3 checker was added to warn about accessing functions that have been
  removed from the itertools module ``izip``, ``imap``, ``iflter``, ``izip_longest``, and ``ifilterfalse``.

  .. code-block:: python

      from itertools import izip
      print(list(izip([1, 2], [3])))

  Instead use ``six.moves`` to import a Python 2 and Python 3 compatible function:

  .. code-block:: python

      from six.moves import zip
      print(list(zip([1, 2], [3])))

* A new Python 3 checker was added to warn about accessing deprecated fields from
  the types module like ``ListType`` or ``IntType``

  .. code-block:: python

      from types import ListType
      print(isinstance([], ListType))

  Instead use the declarations in the builtin namespace:

  .. code-block:: python

      print(isinstance([], list))

* A new Python 3 checker was added to warn about declaring a ``next`` method that
  would have implemented the ``Iterator`` protocol in Python 2 but is now a normal
  method in Python 3.

  .. code-block:: python

      class Foo(object):
          def next(self):
              return 42

  Instead implement a ``__next__`` method and use ``six.Iterator`` as a base class
  or alias ``next`` to ``__next__``:

  .. code-block:: python

      class Foo(object):
          def __next__(self):
              return 42
          next = __next__

* Three new Python 3 checkers were added to warn about using dictionary methods
  in non-iterating contexts.

  For example, the following are returning iterators in Python 3::

  .. code-block:: python

     d = {}
     d.keys()[0]
     d.items()[0]
     d.values() + d.keys()

* A new Python 3 porting check was added, ``non-ascii-bytes-literals``

  This message is emitted whenever we detect that a bytes string contain
  non-ASCII characters, which results in a SyntaxError on Python 3.

* A new warning, ``raising-format-tuple``, will catch situations where the
  intent was likely raising an exception with a formatted message string,
  but the actual code did omit the formatting and instead passes template
  string and value parameters as separate arguments to the exception
  constructor.  So it detects things like

  .. code-block:: python

      raise SomeError('message about %s', foo)
      raise SomeError('message about {}', foo)

  which likely were meant instead as

  .. code-block:: python

      raise SomeError('message about %s' % foo)
      raise SomeError('message about {}'.format(foo))

  This warning can be ignored on projects which deliberately use lazy
  formatting of messages in all user-facing exception handlers.

* Following the recommendations of PEP479_ ,a new Python 3.0 checker was added to warn about raising a ``StopIteration`` inside
  a generator. Raising a ``StopIteration`` inside a generator may be due a direct call
  to ``raise StopIteration``:

  .. code-block:: python

      def gen_stopiter():
          yield 1
          yield 2
          yield 3
          raise StopIteration

  Instead use a simple ``return`` statement

  .. code-block:: python

      def gen_stopiter():
          yield 1
          yield 2
          yield 3
          return

  Raising a ``StopIteration`` may also be due to the call to ``next`` function with a generator
  as argument:

  .. code-block:: python

      def gen_next_raises_stopiter():
          g = gen_ok()
          while True:
              yield next(g)

  In this case, surround the call to ``next`` with a try/except block:

  .. code-block:: python

      def gen_next_raises_stopiter():
          g = gen_ok()
          while True:
              try:
                  yield next(g)
              except StopIteration:
                  return

* The check about raising a StopIteration inside a generator is also valid if the exception
  raised inherit from StopIteration.

  Closes #1385

 .. _PEP479: https://peps.python.org/pep-0479

* A new Python checker was added to warn about using a ``+`` operator inside call of logging methods
  when one of the operands is a literal string:

  .. code-block:: python

     import logging
     var = "123"
     logging.log(logging.INFO, "Var: " + var)

  Instead use formatted string and positional arguments :

  .. code-block:: python

     import logging
     var = "123"
     logging.log(logging.INFO, "Var: %s", var)

* A new Python checker was added to warn about ``inconsistent-return-statements``. A function or a method
  has inconsistent return statements if it returns both explicit and implicit values :

  .. code-block:: python

    def mix_implicit_explicit_returns(arg):
        if arg < 10:
            return True
        elif arg < 20:
            return

  According to PEP8_, if any return statement returns an expression,
  any return statements where no value is returned should explicitly state this as return None,
  and an explicit return statement should be present at the end of the function (if reachable).
  Thus, the previous function should be written:

  .. code-block:: python

    def mix_implicit_explicit_returns(arg):
        if arg < 10:
            return True
        elif arg < 20:
            return None

  Closes #1267

 .. _PEP8: https://peps.python.org/pep-0008

Other Changes
=============

* Fixing u'' string in superfluous-parens message.

* Configuration options of invalid name checker are significantly redesigned.
  Predefined rules for common naming styles were introduced. For typical
  setups, user friendly options like ``--function-naming-style=camelCase`` may
  be used in place of hand-written regular expressions. Default linter config
  enforce PEP8-compatible naming style. See documentation for details.

* Raise meaningful exception in case of invalid reporter class (output format)
  being selected.

* The docparams extension now allows a property docstring to document both
  the property and the setter. Therefore setters can also have no docstring.

* The docparams extension now understands property type syntax.

  .. code-block:: python

      class Foo(object):
          @property
          def foo(self):
              """My Sphinx style docstring description.

              :type: int
              """
              return 10

  .. code-block:: python

    class Foo(object):
        @property
        def foo(self):
            """int: My Numpy and Google docstring style description."""
            return 10

* In case of ``--output-format=json``, the dictionary returned holds a new key-value pair.
  The key is ``message-id`` and the value the message id.

* Spelling checker has a new configuration parameter ``max-spelling-suggestions``, which
  affects maximum count of suggestions included in emitted message.

* The **invalid-name** check contains the name of the template that caused the failure.

  For the given code, **pylint** used to emit ``invalid-name`` in the form ``Invalid constant name var``,
  without offering any context why ``var`` is not such a good name.

  With this change, it is now more clear what should be improved for a name to be accepted according to
  its corresponding template.

* New configuration flag, ``suggestion-mode`` was introduced. When enabled, pylint would
  attempt to emit user-friendly suggestions instead of spurious errors for some known
  false-positive scenarios. Flag is enabled by default.

* ``superfluous-parens`` is no longer wrongly emitted for logical statements involving ``in`` operator
  (see example below for what used to be false-positive).

  .. code-block:: python

    foo = None
    if 'bar' in (foo or {}):
      pass

* Redefinition of dummy function is now possible. ``function-redefined`` message won't be emitted anymore when
  dummy functions are redefined.

* ``missing-param-doc`` and ``missing-type-doc`` are no longer emitted when
  ``Args`` and ``Keyword Args`` are mixed in Google docstring.

* Fix of false positive ``useless-super-delegation`` message when
  parameters default values are different from those used in the base class.

* Fix of false positive ``useless-else-on-loop`` message when break statements
  are deeply nested inside loop.

* The Python 3 porting checker no longer emits multiple ``no-absolute-import`` per file.

* The Python 3 porting checker respects disabled checkers found in the config file.

* Modules, classes, or methods consist of compound statements that exceed the ``docstring-min-length``
  are now correctly emitting ``missing-docstring``

* Fix no ``wrong-import-order`` message emitted on ordering of first and third party libraries.
  With this fix, pylint distinguishes first and third party modules when checking
  import order.

* Fix the ignored ``pylint disable=fixme`` directives for comments following
  the last statement in a file.

* Fix ``line-too-long`` message deactivated by wrong disable directive.
  The directive ``disable=fixme`` doesn't deactivate anymore the emission
  of ``line-too-long`` message for long commented lines.

* If the rcfile specified on the command line doesn't exist, then an
  IOError exception is raised.

* Fix the wrong scope of ``disable=`` directive after a commented line.
  For example when a ``disable=line-too-long`` directive is at the end of a
  long commented line, it no longer disables the emission of ``line-too-long``
  message for lines that follow.
