import _plotly_utils.basevalidators


class XboundsValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(
        self, plotly_name='xbounds', parent_name='pointcloud', **kwargs
    ):
        super(XboundsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='data',
            **kwargs
        )
