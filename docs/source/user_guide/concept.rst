.. _concept:

Concept
-------

The idea of the autocalc framework is to build a dependency-graph from your variables.
Assume you are building some document retrieval app, where users can first select the year
of the document, then based on the year they can select the relevant topic from the list
of topics available for the given year and then they can select the document itself.

In a linear workflow you can assume that users follow the above steps in the above order.
And this is what they will do when they start to work with the app. But when they are
working with the app they might just go back and select a different year. In this case,
the previously generated list of topics is no longer valid, it needs to be reloaded.

The autocalc framwork lets you set up a logical relationship between the document year
and the list of relevant topics, so that the latter gets reloaded when the former is
changed.

Why do we call it a dependency graph? Because in any non-trivial system we won't just
have two variables, but much more. There can be a complex dependency structure between
those variables: variable A may depend on B which depends on C, so as a result A also
depends indirectly on C. So when C changes, both A and B need to be recalculated.

The idea concept may be very similar to you if you work in Excel: If you set a
formula for one cell, this cell will be automatically updated when the value of any cell
in the formula changes.
