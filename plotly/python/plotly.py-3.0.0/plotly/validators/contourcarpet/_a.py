import _plotly_utils.basevalidators


class AValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(self, plotly_name='a', parent_name='contourcarpet', **kwargs):
        super(AValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc+clearAxisTypes',
            implied_edits={'xtype': 'array'},
            role='data',
            **kwargs
        )
