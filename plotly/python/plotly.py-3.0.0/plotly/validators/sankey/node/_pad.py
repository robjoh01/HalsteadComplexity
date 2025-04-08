import _plotly_utils.basevalidators


class PadValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(self, plotly_name='pad', parent_name='sankey.node', **kwargs):
        super(PadValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=False,
            edit_type='calc',
            min=0,
            role='style',
            **kwargs
        )
