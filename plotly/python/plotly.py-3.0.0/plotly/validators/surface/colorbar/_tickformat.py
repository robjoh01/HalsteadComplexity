import _plotly_utils.basevalidators


class TickformatValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self,
        plotly_name='tickformat',
        parent_name='surface.colorbar',
        **kwargs
    ):
        super(TickformatValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='style',
            **kwargs
        )
