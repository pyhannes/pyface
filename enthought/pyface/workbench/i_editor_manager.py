""" The editor manager interface. """


# Enthought library imports.
from enthought.traits.api import Instance, Interface


class IEditorManager(Interface):
    """ The editor manager interface. """

    # The workbench window that the editor manager manages editors for ;^)
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')
    
    def create_editor(self, window, obj):
        """ Create an editor for an object.

        Returns None if no editor can be created for the resource.

        """

    def get_editor(self, window, obj):
        """ Get the editor that is currently editing an object.

        Returns None if no such editor exists.

        """

    def get_editor_memento(self, editor):
        """ Return the state of an editor suitable for pickling etc.

        """
        
    def set_editor_memento(self, memento):
        """ Restore an editor from a memento. """

#### EOF ######################################################################
