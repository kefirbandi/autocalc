from autocalc.autocalc import Var, undefined


def _b(a):
    return 2*a

def test_update():
    a = Var('A', initial_value=1)
    b = Var('B', fun=_b, inputs=[a])
    b_lazy = Var('B_lazy', fun=_b, inputs=[a], lazy=True)

    assert b.get() == 2
    assert b_lazy._get_raw() is undefined
    assert b_lazy.is_undefined()
    assert b_lazy.get() == 2

    a.set(2)
    assert b._get_raw() == 4
    assert b_lazy.is_undefined()
    undefined_inputs = set()
    assert b.get(undefined_inputs) == 4
    assert b_lazy.get() == 4

    assert len(undefined_inputs) == 0

    a.clear()
    assert b._get_raw() is undefined
    assert b.is_undefined()
    undefined_inputs = set()
    assert b.get(undefined_inputs) is undefined

    assert len(undefined_inputs) == 1
    assert a in undefined_inputs