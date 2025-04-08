from plotly.basedatatypes import BaseLayoutHierarchyType
import copy


class Line(BaseLayoutHierarchyType):

    # width
    # -----
    @property
    def width(self):
        """
        Sets the line width. Has an effect only when `type` is set to
        *line*.
    
        The 'width' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        return self['width']

    @width.setter
    def width(self, val):
        self['width'] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return 'layout.mapbox.layer'

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        width
            Sets the line width. Has an effect only when `type` is
            set to *line*.
        """

    def __init__(self, arg=None, width=None, **kwargs):
        """
        Construct a new Line object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            plotly.graph_objs.layout.mapbox.layer.Line
        width
            Sets the line width. Has an effect only when `type` is
            set to *line*.

        Returns
        -------
        Line
        """
        super(Line, self).__init__('line')

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.layout.mapbox.layer.Line 
constructor must be a dict or 
an instance of plotly.graph_objs.layout.mapbox.layer.Line"""
            )

        # Import validators
        # -----------------
        from plotly.validators.layout.mapbox.layer import (line as v_line)

        # Initialize validators
        # ---------------------
        self._validators['width'] = v_line.WidthValidator()

        # Populate data dict with properties
        # ----------------------------------
        v = arg.pop('width', None)
        self.width = width if width is not None else v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))
