autocalc
========

A framework to keep track of dependencies in nonlinear workflows.
`Source code <https://github.com/kefirbandi/autocalc>`_

About
-----

 * Create event-driven apps in Python with ease, without writing callback functions
 * Set up the functional relationship between your public (visible to user) as well as internal (hidden) variables, and
   let autocalc take care of keeping them in sync.

Example
-------

In this example we will implement a quadratic equation solver. User can enter the `a`, `b` and `c` parameters of the


    a*x*x + b*x +c = 0


quadratic equation and we will calculate the two solutions: `x1` and `x2` by the following formulas:


    x1 = (-b-D)/(2a)

    x2 = (-b+D)/(2a)
    
where D is defined as 

    D=sqrt(b*b - 4*a*c)

In this example we assume a Jupyter notebook environment and the use of ipywidgets. The library was designed with this setup in mind, but the core functionality is independent of any interactive environment.

First we declare and display our input variables

.. code-block:: python

    import ipywidgets as widgets
    from autocalc.autocalc import Var
    import math
    
    a = Var('a', initial_value = 1, widget = widgets.FloatText())
    b = Var('b', initial_value = -3, widget = widgets.FloatText())
    c = Var('c', initial_value = 1, widget = widgets.FloatText())

    display(a); display(b); display(c)
    
Then we implement the code which calculates the solution

.. code-block:: python

    def Dfun(a, b, c):
        try:
            return math.sqrt(b*b-4*a*c)
        except ValueError:
            return math.nan
    
    def x1fun(a,b,D):
        return (-b-D)/2/a
    def x2fun(a,b,D):
        return (-b+D)/2/a
    
    
We are now ready to define and display our internal variable: `D=sqrt(b*b - 4*a*c)` and output variables: `x1` and `x2`

.. code-block:: python

    D = Var('D', fun=Dfun, inputs=[a, b, c])
    x1 = Var('X1', fun=x1fun, inputs=[a, b, D], widget =     widgets.FloatText(), read_only=True)
    x2 = Var('X2', fun=x2fun, inputs=[a, b, D], widget = widgets.FloatText(), read_only=True)
    display(x1)
    display(x2)
    
That's it. With just a few lines we set up the dependency graph from our input variables to our output ones. Any time the user upgrades any of the input variables, the output will be updated automatically.

Features
--------

 * Ipywidgets integration + visual framework independent mode of operation.
 * Read-only variables
 * Lightweight, minimal library. Learn the basics in 10 minutes.
 * "Lazy" variables, which only get invalidated when their input(s) change, but are not actually recalculated until explicitly requested. Useful for functions which take a long time to evaluate.
