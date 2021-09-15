Welcome to autocalc documentation!
==================================

Autocalc is a framework aimed primarily at creating apps from your Jupyter notebooks.
The Voila package, which allows you, to turn your notebook into a stand-alone app is gaining popularity as it allows
the creation of apps for scientists and other developers without the need to learn a web framework, or any other library
on top of using the Jupyter notebook which many already know.

Autocalc is not a replacement for Voila. It is a framework that you can use to code the apps that you would like to
publish with Voila.

It allows you to set up the functional relationships between your variables, both the hidden ones and those exposed to
the user via widgets. Once these relationships are set up you can sit back and relax :) as you created an event-driven app.



.. code-block::

    import os
    import ipywidgets as widgets
    from datetime import date
    import pandas as pd

    FREQ = {'Daily': 'B', 'Weekly': 'W-FRI', 'Monthly': 'BM'}

    from autocalc.autocalc import Var

    start_date = Var('Start Date', initial_value = date(2020,9,2), widget = widgets.DatePicker())
    end_date = Var('End Date', initial_value = date(2020,10,2), widget = widgets.DatePicker())
    freq =  Var('Frequency', initial_value='B', widget=widgets.Dropdown(options=FREQ.items()), description='Frequency')

    display(start_date)
    display(end_date)
    display(freq)

    def _dates(start_date, end_date, freq):
        return pd.bdate_range(start_date, end_date, freq=freq)

    dates = Var('Dates', fun=_dates, inputs=[start_date, end_date, freq])

.. toctree::
   :maxdepth: 2

   whats-new.rst
   auto/autocalc

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
