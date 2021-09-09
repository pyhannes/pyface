# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Wx-specific implementation of the text field class """


from traits.api import Any, Instance, Str, provides

import wx

from pyface.fields.i_field import IField, MField
from pyface.ui.wx.layout_widget import LayoutWidget


@provides(IField)
class Field(MField, LayoutWidget):
    """ The Wx-specific implementation of the field class

    This is an abstract class which is not meant to be instantiated.
    """

    #: The value held by the field.
    value = Any()

    #: An optional context menu for the field.
    context_menu = Instance("pyface.action.menu_manager.MenuManager")

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _observe_control_context_menu(self, remove=False):
        """ Toolkit specific method to change the control menu observer. """
        if remove:
            self.control.Unbind(
                wx.EVT_CONTEXT_MENU, handler=self._handle_context_menu
            )
        else:
            self.control.Bind(wx.EVT_CONTEXT_MENU, self._handle_context_menu)

    def _handle_control_context_menu(self, event):
        """ Signal handler for displaying context menu. """
        if self.control is not None and self.context_menu is not None:
            menu = self.context_menu.create_menu(self.control)
            self.control.PopupMenu(menu)
