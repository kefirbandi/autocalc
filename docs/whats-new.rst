What's New
==========

v0.1.0 (unreleased)
-------------------

New Features
~~~~~~~~~~~~
- There is a new ``undefined_inputs`` parameter to the ``get`` and ``recalc`` methods.
  If the function can not be evaluated because some of the inputs are undefined,
  these inputs are collected into this variable.

- The ``PreviewAcc`` class now reports which inputs are missing to calculate the results.

- The ``titles`` parameter of ``PreviewAcc`` now allows to specify an optional 'open'-key, which will be displayed,
  when the Accordion is in an open state.

Bug fixes
~~~~~~~~~
- More robust handling of undefined values with widgets

Internal Changes
~~~~~~~~~~~~~~~~
- Unittests