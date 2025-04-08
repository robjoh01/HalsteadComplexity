import _plotly_utils.basevalidators


class Tick0Validator(_plotly_utils.basevalidators.AnyValidator):

    def __init__(
        self,
        plotly_name='tick0',
        parent_name='scattercarpet.marker.colorbar',
        **kwargs
    ):
        super(Tick0Validator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='colorbars',
            implied_edits={'tickmode': 'linear'},
            role='style',
            **kwargs
        )
