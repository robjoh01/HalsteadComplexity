import _plotly_utils.basevalidators


class FamilysrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(
        self,
        plotly_name='familysrc',
        parent_name='parcoords.hoverlabel.font',
        **kwargs
    ):
        super(FamilysrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='none',
            role='info',
            **kwargs
        )
