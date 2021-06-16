from autocalc.autocalc import Var, undefined
from autocalc.tools import PreviewAcc

def test_var_creation():
    v = Var('_', initial_value=12)
    assert(not v.is_undefined())