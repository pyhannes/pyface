# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


import logging
import sys

from traits.api import Bool, HasTraits, Property, observe, provides, Str

from pyface.qt import QtCore, QtGui
from pyface.i_gui import IGUI, MGUI
from pyface.util.guisupport import get_app_qt4, start_event_loop_qt4


# Logging.
logger = logging.getLogger(__name__)


@provides(IGUI)
class GUI(MGUI, HasTraits):
    """ The toolkit specific implementation of a GUI.  See the IGUI interface
    for the API documentation.
    """

    # 'GUI' interface -----------------------------------------------------#

    application = Property()

    busy = Bool(False)

    started = Bool(False)

    state_location = Str()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, splash_screen=None, name="", icon=None):
        # Change the application icon, if any
        if icon is not None:
            self.set_application_icon(icon)

        # Change the application name, if any
        if name:
            self.set_application_name(name)

        # Display the (optional) splash screen.
        self._splash_screen = splash_screen

        if self._splash_screen is not None:
            self._splash_screen.open()

    # ------------------------------------------------------------------------
    # 'GUI' class interface.
    # ------------------------------------------------------------------------

    @classmethod
    def invoke_after(cls, millisecs, callable, *args, **kw):
        _FutureCall(millisecs, callable, *args, **kw)

    @classmethod
    def invoke_later(cls, callable, *args, **kw):
        _FutureCall(0, callable, *args, **kw)

    @classmethod
    def set_trait_after(cls, millisecs, obj, trait_name, new):
        _FutureCall(millisecs, setattr, obj, trait_name, new)

    @classmethod
    def set_trait_later(cls, obj, trait_name, new):
        _FutureCall(0, setattr, obj, trait_name, new)

    @staticmethod
    def process_events(allow_user_events=True):
        if allow_user_events:
            events = QtCore.QEventLoop.AllEvents
        else:
            events = QtCore.QEventLoop.ExcludeUserInputEvents

        QtCore.QCoreApplication.processEvents(events)

    @staticmethod
    def set_busy(busy=True):
        if busy:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        else:
            QtGui.QApplication.restoreOverrideCursor()

    # ------------------------------------------------------------------------
    # 'GUI' interface.
    # ------------------------------------------------------------------------

    def start_event_loop(self):
        if self._splash_screen is not None:
            self._splash_screen.close()

        # Make sure that we only set the 'started' trait after the main loop
        # has really started.
        self.set_trait_later(self, "started", True)

        logger.debug("---------- starting GUI event loop ----------")
        start_event_loop_qt4()

        self.started = False

    def stop_event_loop(self):
        logger.debug("---------- stopping GUI event loop ----------")
        self.application.quit()

    def set_application_icon(self, image):
        """ Set the application icon in the OS.

        This controls the icon displayed in system docks and similar locations
        within the operating system.
        """
        # ensure application exists before doing anything else
        app = self.application
        app.setWindowIcon(image.create_icon())

    def set_application_name(self, name):
        """ Set the application name at the toolkit level.

        This sets the name displayed for the application in various places
        in the OS.

        Note
        ----
        This does not change the name of the application in the MacOS menu or
        dock.
        """
        self.application.setApplicationDisplayName(name)

    # ------------------------------------------------------------------------
    # Trait handlers.
    # ------------------------------------------------------------------------

    def _state_location_default(self):
        """ The default state location handler. """

        return self._default_state_location()

    @observe("busy")
    def _update_busy_state(self, event):
        """ The busy trait change handler. """
        new = event.new
        if new:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        else:
            QtGui.QApplication.restoreOverrideCursor()

    def _get_application(self):
        return get_app_qt4(*sys.argv)


class _FutureCall(QtCore.QObject):
    """ This is a helper class that is similar to the wx FutureCall class. """

    # Keep a list of references so that they don't get garbage collected.
    _calls = []

    # Manage access to the list of instances.
    _calls_mutex = QtCore.QMutex()

    # A new Qt event type for _FutureCalls
    _pyface_event = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

    def __init__(self, ms, callable, *args, **kw):
        super().__init__()

        # Save the arguments.
        self._ms = ms
        self._callable = callable
        self._args = args
        self._kw = kw

        # Save the instance.
        self._calls_mutex.lock()
        try:
            self._calls.append(self)
        finally:
            self._calls_mutex.unlock()

        # Move to the main GUI thread.
        self.moveToThread(QtGui.QApplication.instance().thread())

        # Post an event to be dispatched on the main GUI thread. Note that
        # we do not call QTimer.singleShot here, which would be simpler, because
        # that only works on QThreads. We want regular Python threads to work.
        event = QtCore.QEvent(self._pyface_event)
        QtGui.QApplication.postEvent(self, event)

    def event(self, event):
        """ QObject event handler.
        """
        if event.type() == self._pyface_event:
            if self._ms == 0:
                # Invoke the callable now
                try:
                    self._callable(*self._args, **self._kw)
                finally:
                    # We cannot remove from self._calls here. QObjects don't like being
                    # garbage collected during event handlers (there are tracebacks,
                    # plus maybe a memory leak, I think).
                    QtCore.QTimer.singleShot(0, self._finished)
            else:
                # Invoke the callable (puts it at the end of the event queue)
                QtCore.QTimer.singleShot(self._ms, self._dispatch)
            return True

        return super().event(event)

    def _dispatch(self):
        """ Invoke the callable.
        """
        try:
            self._callable(*self._args, **self._kw)
        finally:
            self._finished()

    def _finished(self):
        """ Remove the call from the list, so it can be garbage collected.
        """
        self._calls_mutex.lock()
        try:
            self._calls.remove(self)
        finally:
            self._calls_mutex.unlock()
