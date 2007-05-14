#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" Abstract base class for all action managers. """


# Enthought library imports.
from enthought.traits.api import Constant, Event, HasPrivateTraits, Instance
from enthought.traits.api import List, Property, Str

# Private Enthought library imports.
from enthought.pyface.toolkit import patch_toolkit

# Local imports.
from action_controller import ActionController
from group import Group


class ActionManager(HasPrivateTraits):
    """ Abstract base class for all action managers.

    An action manager contains a list of groups, with each group containing a
    list of items.

    There are currently three concrete sub-classes, 'MenuBarManager',
    'MenuManager' and 'ToolBarManager'.

    """

    #### 'ActionManager' interface ############################################

    # The Id of the default group.
    DEFAULT_GROUP = Constant('additions')

    # The action controller (if any) used to control how actions are performed.
    controller = Instance(ActionController)

    # All of the contribution groups in the manager.
    groups = Property(List(Group))

    # The manager's unique identifier (if it has one).
    id = Str

    #### Events ####

    # fixme: We probably need more granular events than this!
    changed = Event

    #### Private interface ####################################################

    # All of the contribution groups in the manager.
    _groups = List(Group)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *args, **traits):
        """ Creates a new menu manager. """

        # Base class constructor.
        super(ActionManager, self).__init__(**traits)

        # The last group in every manager is the group with Id 'additions').
        #
        # fixme: The side-effect of this is to ensure that the 'additions'
        # group has been created.  Is the 'additions' group even a good idea?
        self._get_default_group()

        # Add all items to the manager.
        group = None
        for arg in args:
            # We allow a group to be defined by simply specifying a string (its
            # Id).
            if isinstance(arg, basestring):
                # Create a group with the specified Id.
                arg = Group(id=arg)

            # If the item is a group then add it just before the default group
            # (ie. we always keep the default group as the last group in the
            # manager).
            if isinstance(arg, Group):
                self.insert(-1, arg)
                group = arg

            # Otherwise, the item is an action so add it to the current group.
            else:
                # If no group has been created then add one.  This is only
                # relevant when using the 'shorthand' way to define menus.
                if group is None:
                    group = Group(id='__first__')
                    self.insert(-1, group)

                group.append(arg)

        return

    ###########################################################################
    # 'ActionManager' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_groups(self):
        """ Returns the groups in the manager. """

        return self._groups[:]

    #### Methods ##############################################################

    def append(self, item):
        """ Appends an item to the manager.

        See the documentation for 'insert'.

        """

        return self.insert(len(self._groups), item)

    def destroy(self):
        """ Called when the manager is no longer required.

        By default this method simply calls 'destroy' on all of the manager's
        groups.

        """

        for group in self.groups:
            group.destroy()
        
        return

    def insert(self, index, item):
        """ Inserts an item into the manager at the specified index.

        The item can be:-

        1) A 'Group' instance.

            In which case the group is inserted into the manager's list of
            groups.

        2) A string.

            In which case a 'Group' instance is created with that Id, and then
            inserted into the manager's list of groups.

        3) An 'ActionManagerItem' instance.

            In which case the item is inserted into the manager's default
            group.

        """

        # 1) The item is a 'Group' instance.
        if isinstance(item, Group):
            group = item

            # Insert the group into the manager.
            group.parent = self
            self._groups.insert(index, item)

        # 2) The item is a string.
        elif isinstance(item, basestring):
            # Create a group with that Id.
            group = Group(id=item)

            # Insert the group into the manager.
            group.parent = self
            self._groups.insert(index, group)

        # 3) The item is an 'ActionManagerItem' instance.
        else:
            # Find the default group.
            group = self._get_default_group()

            # Insert the item into the default group.
            group.insert(index, item)

        return group

    def find_group(self, id):
        """ Returns the group with the specified Id.

        Returns None if no such group exists.

        """

        for group in self._groups:
            if group.id == id:
                break

        else:
            group = None

        return group

    def find_item(self, path):
        """ Returns the item found at the specified path.

        'path' is a '/' separated list of contribution Ids.

        Returns None if any component of the path is not found.

        """

        components = path.split('/')

        # If there is only one component, then the path is just an Id so look
        # it up in this manager.
        if len(components) > 0:
            item = self._find_item(components[0])

            if len(components) > 1 and item is not None:
                item = item.find_item('/'.join(components[1:]))

        else:
            item = None

        return item

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_default_group(self):
        """ Returns the manager's default group. """

        group = self.find_group(self.DEFAULT_GROUP)
        if group is None:
            group = Group(id=self.DEFAULT_GROUP)
            self.append(group)

        return group

    def _find_item(self, id):
        """ Returns the item with the specified Id.

        Returns None if no such item exists.

        """

        for group in self.groups:
            item = group.find(id)
            if item is not None:
                break

        else:
            item = None

        return item

    ###########################################################################
    # Debugging interface.
    ###########################################################################

    def dump(self, indent=''):
        """ Render a manager! """

        print indent, 'Manager', self.id
        indent += '  '

        for group in self._groups:
            self.render_group(group, indent)

        return

    def render_group(self, group, indent=''):
        """ Render a group! """

        print indent, 'Group', group.id
        indent += '    '

        for item in group.items:
            if isinstance(item, Group):
                self.render_group(item, indent)

            else:
                self.render_item(item, indent)

        return

    def render_item(self, item, indent=''):
        """ Render an item! """

        if hasattr(item, 'groups'):
            item.dump(indent)

        else:
            print indent, 'Item', item.id

        return

#### EOF ######################################################################
