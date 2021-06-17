import ipywidgets as widgets
from autocalc.autocalc import Var

def test_widget_init():
    text_widget = widgets.Text()
    t = Var('T', initial_value='text', widget=text_widget)
    assert text_widget.value == 'text'

    t.set('-')
    assert text_widget.value == '-'

    text_widget.value = '+'
    assert t.get() == '+'
