import ipywidgets as widgets
from IPython.display import display, clear_output
from autocalc.autocalc import Var, undefined


class PreviewAcc(widgets.Accordion):
    def __init__(self, titles:dict, value_var:Var):
        """

        :param titles: a dict like {'defined': 'Show the calculated value', 'undefined':'Calculate and show the value'}
        :param value_var: The Var to display
        """
        self.box=widgets.Output()
        widgets.Accordion.__init__(self, children=[self.box])

        self.selected_index = None
        self.set_title(0, titles['undefined'])
        self.titles = titles
        self.value_var = value_var

        # setting the initial value to anything but undefined will keep the function from evaluating it at start
        Var(f'PreviewAccAction[{value_var.name}])', fun=self._preview, inputs=[value_var], undefined_input_handling='function', initial_value=None)
        self.observe(self.p, 'selected_index')

    def _preview(self, value):
        if value is undefined:
            self.set_title(0, self.titles['undefined'])
            self.selected_index = None
        else:
            self.set_title(0, self.titles['defined'])

    def p(self, *args):
        si = args[0]['new']
        if si == 0:  # Acc was opened
            with self.box:
                clear_output()
                print('Loading ...')

            undefined_inputs = set()
            z = self.value_var.get(undefined_inputs=undefined_inputs)

            with self.box:
                clear_output()
                if z is undefined:
                    if len(undefined_inputs):
                        ui_str = '", "'.join(map(lambda x: x.name, undefined_inputs))
                        msg = f'Could not calculate {self.value_var.name}, because the following inputs are undefined: "{ui_str}".'
                    else:
                        msg = 'Could not calculate {self.value_var.name} for some reason'
                    print(msg)
                else:
                    display(z)
            if 'open' in self.titles:
                self.set_title(0, self.titles['open'])
        elif si is None:
            self._preview(self.value_var._get_raw())