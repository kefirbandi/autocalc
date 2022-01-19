import warnings

from IPython.display import display
from ipywidgets import FloatText, FileUpload, Button, HBox, DatePicker
import math

UNDEFINED_WIDGET_STATES=[(FloatText,math.nan), (DatePicker,None)]

class _Undefined:
    def __str__(self):
        return '<Undefined Value>'

    __repr__ = __str__

#: The undefined value
undefined = _Undefined()

def _check_undefined(fun):
    """
    Decorator to return an undefined value in case any of the inputs is undefined.
    """
    if fun is None:
        return None

    def decorated(*args):
        for arg in args:
            if arg is undefined:
                return undefined
        else:
            return fun(*args)
    return decorated

class _SharedVariable:
    """
    The idea is to create a "mutable variable"
    """
    def __init__(self,v):
        self.var=v

    def get(self):
        return self.var

    def set(self, v):
        self.var = v


class Var:
    def __set_name__(self, owner, name):
        """
        Will be called automatically, after __init__, when the object is specified as a class level variable.
        Part of the descriptor variable framework
        """
        self.name = name

    in_widget_handling = _SharedVariable(False)

    def __init__(self, name:str=None, *, fun=None, inputs=[], initial_value=undefined, lazy:bool=False, widget=None,
                 read_only:bool=False, description:str='', undefined_input_handling:str='undefined'):
        """

        :param name: Used for display purposes only. E.g. when using display()
        :type name: str
        :param fun: The function which generates this var
        :param inputs: The list of input Vars, in the order required by` fun`
        :type inputs: List of Vars
        :param initial_value: Initial value
        :param lazy: If set to True, then the Var value will not be automatically computed when any of the inputs change.
         In this case it will be set to "undefined". Calculation can be triggered using the `.get` method
        :param widget: The widget associated with this Var. Note: do not set an initial value for this widget.
         Rather use the `initial_value` parameter of the Var. It will set the widget state accordingly.
        :param read_only: If set to true then it will not be allowed to change the value of the Var with the `.set` method
         or through the widget. This flag will also set the widget (if given) to disabled.
         If the Var depends on other Vars, any change in those will trigger a recalculation. Only the direct modification
         is disabled.
         Note, that setting this flag is not equivalent to disabling the widget, because if the flag is set then the `.set`
         method is also disabled not only the widget.
        :param description: A description string to be shown as a tooltip when using `display()` on the widget.
        :param undefined_input_handling: This parameter specifies what to do when any of the inputs is undefined.
         (Either because it is lazily computed, or can't be computed for any reason.)
         * The default setting is 'undefined' which means that the function will NOT be executed and the output will
         be `undefined`.
         * If set to 'function' then the function will be executed with potentially undefined inputs. In the function
           one can test for a parameter being undefined using `input1 is undefined`
        """
        self.name = name # Only for display purposes
        if undefined_input_handling == 'undefined':
            self.fun = _check_undefined(fun) # How to update the value
        elif undefined_input_handling == 'function':
            self.fun = fun
        else:
            raise ValueError('The undefined_input_handling parameter should be either "undefined" or "function",')
        self.description = description

        self.depend_on_me=set() # The
        self.inputs = inputs
        for d in inputs:
            d.depend_on_me.add(self)
        self.lazy = lazy
        self.widget = widget
        if widget is not None:
            for k, v in UNDEFINED_WIDGET_STATES:
                if isinstance(widget, k):
                    self.widget_default = v
                    break
            else:
                self.widget_default = widget.value
            widget.observe(lambda change:self._widget_changed(), names='value')
        self.read_only = read_only
        if read_only and widget is not  None:
            self.widget.disabled = True


        # Var just created. No other Var depends on it yet, so no need to update anything upstream.
        # Just set or recalculate the value
        self._set_raw(initial_value, skip_updating_this_widget= initial_value is undefined) # The underlying value
        if (initial_value is undefined) and (not lazy) and (self.fun is not None):
            self._recalc_this_node_only()

        # self.outer_obj = None

    converters = [(FileUpload, lambda value: list(value.values())[0]['content'].decode())]
    def _read_widget_value(self):
        for k, v in UNDEFINED_WIDGET_STATES:
            if isinstance(self.widget, k):
                if self.widget.value == self.widget_default:
                    return undefined

        for k,v in self.converters:
            if isinstance(self.widget, k):
                converter = v
                break
        else:
            converter = lambda x : x
        return converter(self.widget.value)

    def _widget_changed(self):
        if not self.in_widget_handling.get():
            self.in_widget_handling.set(True)
            self.set(self._read_widget_value(), skip_updating_this_widget=True) # -> widget value already set, no need to set it again
            # self.set(self.widget.value, skip_updating_this_widget=True) # -> widget value already set, no need to set it again
            self.in_widget_handling.set(False)


    def __str__(self):
        return f'{self.name}({self._get_raw()})'

    __repr__ = __str__

    def _get_calculation_order_dict(self, nodes=None):
        """
        This returns a dictionary with Var -> int.
        The idea is that we need to start calculating with the lowest values and increase monotonically.
        This way we can be sure, that for each node (Var) the inputs are recalculated
        :param nodes:
        :return:
        """
        my_co = {self:0}
        if nodes is None:
            nodes = self.depend_on_me
        for d in nodes:
            co = d._get_calculation_order_dict()
            for k,v in co.items():
                my_co[k] = max(my_co.get(k,0), v+1)

        return my_co

    def _get_calculation_order_list(self, nodes=None):
        """
        This turns the calculation order dict into a list of sets
        We should start calculation with the first set, then the second, etc.
        :param nodes:
        :return:
        """
        co = self._get_calculation_order_dict(nodes)
        depth = max(co.values())
        ll=[ set() for _ in range(depth) ]
        for k,v in co.items():
            if v:
                ll[v-1].add(k)
        return ll

    def _invalidate(self):
        self._set_raw(undefined)

    def clear(self):
        """
        Sets the Var to the undefined state
        :return:
        """
        self.set(undefined)

    def _get_raw(self):
        return self._v

    def _set_raw(self, value, skip_updating_this_widget=False):
        self._v = value
        if (not skip_updating_this_widget) and (self.widget is not None):
            # Have to make sure, whenever we change a widget from code, this does not trigger any recalculation
            # This is because we explicitly do the recalculations in the code.
            # If we came here because user changed the widget, then widget handling is already turned off.
            # But below we prepare for the case when change is initiated from code.
            # In any case we set the widget_handling to True, signalling that the change of value we initiate here
            # should not trigger any updates.
            prev_state = self.in_widget_handling.get()
            self.in_widget_handling.set(True)
            if self.is_undefined():
                self.widget.value = self.widget_default
            else:
                self.widget.value = value
            self.in_widget_handling.set(prev_state)

    def set(self, value, skip_updating_this_widget=False):
        """
        Set the value and do the housekeeping: all those who depend on us either explicitly or implicitly
        need to be either updated or recalculated.
        """
        if self.read_only:
            return

        same = self._get_raw() == value
        try:
            same = bool(same)
        except ValueError:
            try:
                same = same.all()
            except AttributeError:
                same = False

        if same:
            return

        self._set_raw(value, skip_updating_this_widget)
        my_co = self._get_calculation_order_list()
        for items in my_co:
            for ii in items:
                ii._recalc_this_node_only()

    def is_undefined(self):
        return self._get_raw() is undefined

    def get(self, undefined_inputs=None):
        """

        Returns: The current value if set, or triggers the calculation and the returns the value if undefined.
        Note, that this function may return undefined, depending on circumstances.

        """
        if undefined_inputs is None:
            undefined_inputs = set()
        if (self.fun is not None) and self.is_undefined():
            self._recalc_explicite(False, undefined_inputs)
        return self._get_raw()

    def recalc(self, undefined_inputs=None):
        """
        The difference between `.get` and `.recalc` is that the latter triggers a function evaluation
        even if the value is not undefined.
        May be needed in cases, when the Var depends on other Vars, but may also be overwritten directly.

        """
        if undefined_inputs is None:
            undefined_inputs = set()
        if (self.fun is not None):
            self._recalc_explicite(True, undefined_inputs)
        return self._get_raw()


    def _recalc_explicite(self, force=False, undefined_inputs=None):
        """
        Do our best to recalc, not just lazily: if something is missing from below,
        do a recalc there as well
        :return:
        """
        # This is the recursive part, where we walk strictly down on our dependencies
        # We collect those nodes which have changed
        if undefined_inputs is None:
            undefined_inputs = set()
        changed = set()
        # By the following function we set our own value. But the function goes down recursively
        # to set the value of our dependencies (before calculating our value of course) if possible.
        # Also collects those nodes, which have changed (= their values was set).
        self._calc_and_collect(changed, force, undefined_inputs)

        # Now for those values which are upstream (depend on us) to any of those which have changed we need to recalculate those.
        # This is because we require that at every point in time when we finish an internal function all nodes
        # should be consistent: either the correct value of "undefined" for lazy nodes.
        my_co = self._get_calculation_order_list(changed)
        for items in my_co:
            for ii in items:
                if ii not in changed:
                    ii._recalc_this_node_only()

    def _calc_and_collect(self, changed, force=False, undefined_inputs=None):
        """
        Calculate the value of this node, and (before that) recursively the value of nodes on which this node depends.
        Also collect the nodes which have changed in the accumulator variable "changed", which is a set.
        :param changed:
        :return:
        """
        if undefined_inputs is None:
            undefined_inputs = set()
        if (self.is_undefined() and self.inputs) or force: #i.e. we should try to update ourselves
            values = [v._calc_and_collect(changed, undefined_inputs=undefined_inputs) for v in self.inputs]
            v = self.fun(*values)
            if v is not undefined:
                self._set_raw(v)
                changed.add(self)
        if self.is_undefined() and not self.inputs:
            undefined_inputs.add(self)
        return self._get_raw()


    def _recalc_this_node_only(self):
        if self.lazy:
            self._invalidate()
        else:
            values = [v._v for v in self.inputs]
            v = self.fun(*values)
            self._set_raw(v)

    @property
    def widget_set(self):
        """
        Returns the "thing" that you can put inside `display` or `HBox`.
        :return:
        """
        if self.widget is not None:
            widget = self.widget
            name = self.name
            help = self.description
            label = Button(disabled=True, description=name)
            if help:
                label.description += ' (?)'
                label.tooltip = help
            label.style.button_color = 'lightgreen'
            return HBox([label, widget])
        else:
            return self._get_raw()

    @property
    def w(self):
        warnings.warn('The "w" field of Var is deprecated. Please use "widget_set" instead.')
        return self.widget_set

    def _ipython_display_(self):
        display(self.widget_set)
