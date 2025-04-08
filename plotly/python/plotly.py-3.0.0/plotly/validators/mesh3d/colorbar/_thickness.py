import _plotly_utils.basevalidators


class ThicknessValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='thickness', parent_name='mesh3d.colorbar', **kwargs
    ):
        super(ThicknessValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='colorbars',
            min=0,
            role='style',
            **kwargs
        )
