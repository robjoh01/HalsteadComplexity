import _plotly_utils.basevalidators


class LowValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(self, plotly_name='low', parent_name='ohlc', **kwargs):
        super(LowValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='data',
            **kwargs
        )
