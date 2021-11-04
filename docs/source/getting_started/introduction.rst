Introduction
------------
Purpose
.......

The purpose of the autocalc package is to help the creator of Python-based interactive app developers (primarily those
using Jupyter notebook) by providing a framework to set-up the dependencies between their internal
and external variables.

Ok, now what does this mean? Building an app requires interaction from the user. Output values (numbers, graphs, tables,
etc.) are based on the input parameters either directly or indirectly through other variables, hidden from the user.
As long as the user specifies the variables in their "proper order" all other variables can be calculated in
the order which is specified by their dependencies, or dependency-graph, if you like.
But what happens if user changes the value of an already defined input parameter? All other variables
(internal, or public) which depend on it either directly or indirectly need to be recalculated.

Without the use of autocalc or a similar framework the user would need to implement tons of callback functions
, which would need to be maintained whenever new variables are introduced in the system. Note, that the code
also needs to properly update variables which depend indirectly on the input parameters. Coding and
maintaining these callback functions can easily become a nightmare.

That's where autocalc comes to help. Define the depencies and the functional relationships between your
variables using a very simple construct and let the framework take care of keeping your variables in sync.
Think in terms of "what", not "how"! Build interactive apps with with minimal (even zero) callback functions!

Do you know Excel?
..................

Think about Excel and other similar spreadsheet apps. The main idea is to make the value of cells depend on
other cells. You don't need to write any VBA to keep those cells in sync! Same with autocalc: set up the
dependency graph and let the library take care of the rest!

Why autocalc?
.............

Although other similar frameworks exist, where autocalc shines is its simplicity: use a single language
construct to set up the dependency graph. 
