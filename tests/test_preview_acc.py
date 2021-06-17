from autocalc.autocalc import Var
from autocalc.tools import PreviewAcc

call_counter = []


def calculate(x):
    call_counter.append(1)
    return 2*x


def test_preview_acc():
    in_var = Var('I', initial_value='A')
    out_var = Var('O', fun=calculate, inputs=[in_var], lazy=True)

    p = PreviewAcc({'defined': 'defined', 'undefined': 'undefined', 'open': 'open'}, out_var)

    # Initial widget state
    assert p.selected_index is None
    assert p.get_title(0) == 'undefined'
    assert len(call_counter) == 0

    # Opening the acc
    p.selected_index = 0
    assert p.selected_index == 0
    assert p.get_title(0) == 'open'
    assert len(call_counter) == 1

    # Closing the acc
    p.selected_index = None
    assert p.selected_index is None
    assert p.get_title(0) == 'defined'
    assert len(call_counter) == 1

    # Reopening
    p.selected_index = 0
    assert len(call_counter) == 1

    # Clearing the input value
    in_var.clear()
    assert p.selected_index is None

    # Opening
    p.selected_index = 0
    assert p.get_title(0) == 'open'
    assert len(call_counter) == 1

    # Changing the input
    in_var.set('B')
    assert p.selected_index is None

    # Opening
    p.selected_index = 0
    assert p.get_title(0) == 'open'
    assert len(call_counter) == 2

    p.selected_index = None
    assert p.get_title(0) == 'defined'

    # Changing the input again
    in_var.set('C')
    assert p.selected_index is None

    # Opening
    p.selected_index = 0
    assert p.get_title(0) == 'open'
    assert len(call_counter) == 3


