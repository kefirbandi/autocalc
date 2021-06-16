from autocalc.autocalc import Var, undefined


def test_basic_operation():
    v = Var('_', initial_value=12)
    assert(not v.is_undefined())
    assert(v.get() == 12)
    assert(v.recalc() == 12)

    v.set(23)
    assert (v.get() == 23)

    v.clear()
    assert(v.is_undefined())

    assert(v.get() is undefined)
