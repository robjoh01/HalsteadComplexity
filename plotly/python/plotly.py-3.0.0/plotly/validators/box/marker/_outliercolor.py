import _plotly_utils.basevalidators


class OutliercolorValidator(_plotly_utils.basevalidators.ColorValidator):

    def __init__(
        self, plotly_name='outliercolor', parent_name='box.marker', **kwargs
    ):
        super(OutliercolorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='style',
            role='style',
            **kwargs
        )
