.. _widgets:

Using widgets to interact with autocalc
---------------------------------------

Using widgets is relatively straightforward. At the moment autocalc only supports Ipywidgets.
Simply define the value of the `widget` parameter when defining your Var::

    name_input=Var('Your name', description='Enter your name', widget=widgets.Text())

It is your responsibility to display the widget when and where you wish, which you
can refer to as `name_input.widget`.

There is one feature, which autocalc provides: you can `display` the Var itself, like::

    display(name_input)

This will display not only the widget, but will also put a label in front of it showing
its name and its optional description when hovered over.

If you would like to get access to the set of widgets display by the `display`
function you can get it with the `.w` member. E.g.::

    display(HBOX([some_other_widget, name_input.w]))


When using the widgets, you don't need to use explicit `.set()` and `.get()` methods as
they are handled by autocalc. Except when using :ref:`lazy_variables`, in which case
the `.get()` method needs to be called explicitly.

Undefined values
................

Note, that the state of the Var may be :ref:`undefined<undefined>`. This state can not be
intuitively represented by most of the widgets. E.g. an empty TextBox can't be distinguished
from an undefined one. But be assured, the state of the Var will be undefined.

