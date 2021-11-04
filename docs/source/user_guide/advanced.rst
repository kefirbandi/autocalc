.. _advanced:

Advanced features
-----------------

.. _lazy_variables:

Lazy variables
..............

In many cases there are some variables, which depend on more than one input variable and
are slow to calculate. In these cases it is usually not the best approach to recalculate
them every time when one of their input changes. It is a waste of resources and gives a frustrating experience to the user.

We will can flag such variables with the "lazy" flag, by setting their `lazy` flag to True::

    my_slow_var = Var('MY_VAR', fun=my_fun, inputs=[a, b], lazy=True)

For such variables, the function will only be evaluated once the user calls the `.get()`
method explicitly. In an interactive Jupyter interface this can easily be achieved by
adding a "Calc" button, whose action is to call `.get()` on the relevant Var.

Another option is to use the :class:`autocalc.tools.PreviewAcc` class, which is derived from 
`ipywidgets.Accordion` and does a recalculation when the Accordion is opened.


Note, that although lazy variables are not recalculated when one of their inputs change, leaving them with the previous value would result in an inconsistent state. In this case this vars will be invalidated and assigned an "undefined" state, which brings us to the next topic:

.. _undefined:

Undefined variables
...................

The Vars you defined do not necessarily have a value. For example they may be input variables, where user input is expected, or lazily calculated variables before triggering their
recalculation. Such variables are in an undefined state (my_var.is_undefined() evaluates to True). Ideally all values are defined before they are being used, but is in everyday 
situation that user skips the setting of some relevant variables and so the calculation 
cannot be performed.

In order to be prepared for such cases in our UI we can either directly inquire the
relevant variables and check their state through the `.is_undefined` method, or more
conveniently can pass in a Python `set` object as the optional `undefined_inputs`
parameter of the `.get()` method, which will collect all necessary but undefined objects.

Note, that a Var can be explicitly invalidated by using the `.clear()` method.


By default, the calculation of a Vars function is not triggered when any of its inputs is
not defined. However, there may be cases, when depending on the value of some other parameters,
one of the inputs parameters value is not relevant. E.g.::

    def custom_function(a, b):
        if a > 5:
            return a
        else:
            return b

For such cases the user may allow the calculation of such functions by setting the
`undefined_input_handling` parameter of the Var constructor to 'function'.
To guard against unexpected errors during function evaluation one can check whether a
value is undefined using the `is undefined` syntax, like::

    from autocalc.autocalc import undefined

    def custom_function(a, b):
        if a is undefined:
            return undefined
        if a > 5:
            return a
        else:
            if b is undefined:
                return undefined
            else:
                return b

