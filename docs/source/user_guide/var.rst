.. _var:

The Var object
--------------

Fortunately for you, the autocalc package is very easy to use:
There is one single class (:class:`Var<autocalc.autocalc.Var>`) which you need to learn in order to utilize its features.

`Var` is a wrapper around any variable which you would like to be part of the
dependency-graph. In addition to holding the variable, it stores all the necessary
information to describe the position of the variable in the graph (ie. its neighbors
upstream and downstream) some meta-data (e.g. default value) and the corresponding widget
if any.

The task
........


So let's dive into it and build an app to calculate the roots of a quadratic equation:
:math:`ax^2 + bx + c = 0`. During this process we will introduce the `Var` object.

Remember, that the solutions are given by:

 * :math:`x_1 = \frac{-b + D}{2a}`, and
 * :math:`x_2 = \frac{-b - D}{2a}`, where
 * :math:`D = \sqrt{b^2 - 4ac}`.

In this example we will concentrate on real roots only, excluding complex ones.
First we will give a "widget-less" solution, where we will use pure Python methods to
manipulate the values. This will enable us to introduce the "low-level" interface to `Var`
objects. Adding interactivity through widgets is straightforward and will be shown
in section :ref:`widgets`.

Imports
.......

As far as the autocalc package is concerned we need to import the `Var` object only::

    from autocalc.autocalc import Var

For this particular example we additionally need::

    import math

Input variables
...............

The variables `a`, `b` and `c` are pure input variables, they do not depend on others,
so they can simply be defined as::

    a = Var('a', initial_value = 1)
    b = Var('b', initial_value = -3)
    c = Var('c', initial_value = 1)

The first, positional, argument to `Var` is its name. You can give arbitrary names to
the Vars, they don't need to be distinct. They are only used when displaying the
Var. All other arguments are keyword-only.

Calculated variables
....................

The next Var we will introduce is `D`. It is calculated from `a`, `b` and `c` by the
following function::

    def Dfun(a, b, c):
        try:
            return math.sqrt(b*b-4*a*c)
        except ValueError:
            return math.nan

The corresponding Var is defined as::

    D = Var('D', fun=Dfun, inputs=[a, b, c], read_only=True)

For `D` we had to define the function, which is used to calculate it, as well as the
input Vars which need to be bound to the function. The `inputs` argument to `Var` is a
list, the order needs to match the order of the positional arguments of the function.

Read-only variables
...................

Note the we set `D` to be a `read-only` variable. It means, that its value can change,
but only through its inputs; it is not allowed to change its value directly.
At first it may seem obvious that if a value is a function of other variables
then it should be read-only. However, there may be cases when the function value only
gives a "default" value, which the user may override. For example: in your app you
load a custom configuration file and you set your `custom_configuration_xml` variable
accordingly. It is natural to set your `use_custom_configuration` boolean variable to `True`
whenever the `custom_configuration_xml` variable changes as you can assume, that the user
set a custom value in order to use it. So the `use_custom_configuration` variable depends
on `custom_configuration_xml` variable trough some function which e.g. checks the
correctness of `custom_configuration_xml` and returns `True` if it succeeds.
This will assure that `use_custom_configuration`
will be reset to `True` whenever `custom_configuration_xml` changes, as we can assume
that the user just set it in order to use it.
However you want to give the user the chance to switch off the usage of the custom
configuration without
having to manipulate the `custom_configuration_xml` variable. So in this case
`use_custom_configuration` is the result of another variable but can also be overwritten
manually.

The reason why we introduced `D` is to share the results between the two solutions:
:math:`x_1` and :math:`x_2`. (Actually the real reason is to show you how this can be
done :) )

Solutions
.........

The two solutions (:math:`x_1` and :math:`x_2`) can also be defined with the help of
calculation functions and their corresponding inputs as::

    def x1fun(a,b,D):
        return (-b-D)/2/a
    def x2fun(a,b,D):
        return (-b+D)/2/a

    x1 = Var('X1', fun=x1fun, inputs=[a, b, D], read_only=True, description='The first solution of the equation')
    x2 = Var('X2', fun=x2fun, inputs=[a, b, D], read_only=True, description='The second solution of the equation')

So, as you can see, :math:`x_1` and :math:`x_2` depend on `a`, `b` and `D` and through
`D` also indirectly on `c`.
Also note, that we can add a descritpion to the Var, which will be used when displaying
the Var in  Jupyter notebook. See :ref:`widgets`.

Reading and writing the variables
.................................

So by now we've set up our variables, but how do we give values to them and how do we
read their values? This would be trivial if we used :ref:`widgets<widgets>`, but this is not the
only way we can do these operaions.

Reading and writing the variables is achieved through the `.set` and `.get` methods::

    a.set(10)
    b.set(-12)
    print(x1.get())
    print(a.get()*x1.get()*x1.get() + b.get()*x1.get() + c.get())

We also need to mention the `.recalc()` method which will force a recalculation
of the value, even if the value is already calculated. This may be useful for those
"non read-only" Vars which depend on other Vars and we would like to reset their
"default" value.

We also need to mention the optional output variable `undefined_inputs` of the
`.get()` method. If a set is passed as input then it will collect all other
Vars on which directly or indirectly this Var depends but are in an :ref:`Undefined <undefined>` state and therefore do not allow the calculation of this Var.
This can be used for "debugging" purposes on the user level, i.e. to give
a meaningful message to the user as to why the calculation failed.




