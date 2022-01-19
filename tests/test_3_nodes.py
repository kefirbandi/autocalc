from autocalc.autocalc import Var

# c depends on b, which depends on a
# a -> b -> c
def double(x):
    return 2*x

class EC():
    def __init__(self):
        self.execution_count = 0

    @property
    def executed(self):
        v = self.execution_count
        self.execution_count = 0
        return v

    def fun(self, x):
        self.execution_count += 1
        return 2*x


def test_proper_function_triggering():
    ecB = EC()
    ecC = EC()
    a = Var('A', initial_value=1)
    b = Var('B', fun=ecB.fun, inputs=[a])
    assert ecB.executed
    c = Var('C', fun=ecC.fun, inputs=[b])
    assert not ecB.executed
    assert ecC.executed

    assert c._get_raw() == 4
    assert c.get() == 4

    assert not ecB.executed
    assert not ecC.executed

    b.set(6)

    assert not ecB.executed
    assert ecC.executed

    assert c._get_raw() == 12
    assert a._get_raw() == 1

    a.set(2)

    assert ecB.executed
    assert ecC.executed

    assert c.get() == 8
    assert not ecC.executed


