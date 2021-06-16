import ipywidgets as widgets
from IPython.display import display, clear_output
from autocalc.autocalc import Var, undefined


class PreviewAcc(widgets.Accordion):
    def __init__(self, titles, value_var):
        self.box=widgets.Output()
        widgets.Accordion.__init__(self, children=[self.box])

        self.selected_index = None
        self.set_title(0, titles['undefined'])
        self.titles = titles
        self.value_var = value_var

        Var('_', fun=self._preview, inputs=[value_var], undefined_input_handling='function')
        self.observe(self.p)

    def _preview(self, value:Var):
        if value is undefined:
            self.set_title(0, self.titles['undefined'])
            self.selected_index = None
        else:
            self.set_title(0, self.titles['defined'])

    def p(self, *args):
        z = args[0]['new']
        if isinstance(z, dict):
            si = z.get('selected_index')
            if si == 0:  # Acc was opened
                with self.box:
                    clear_output()
                    print('Loading ...')
                    clear_output(wait=True)
                    z = self.value_var.get()
                    clear_output()
                    display(z)