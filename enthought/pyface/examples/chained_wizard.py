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
""" Chained wizard example. """


# Standard library imports.
import os, sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))

# Enthought library imports.
from enthought.pyface.api import GUI, OK
from enthought.pyface.wizard.api import ChainedWizard, SimpleWizard, WizardPage
from enthought.traits.api import Color, HasTraits, Int, Str



class Details(HasTraits):
    """ Some test data. """

    name = Str
    color = Color


class SimpleWizardPage(WizardPage):
    """ A simple wizard page. """

    #### 'SimpleWizardPage' interface #########################################

    # The page color.
    color = Color

    ###########################################################################
    # 'WizardPage' interface.
    ###########################################################################

    def create_page(self, parent):
        """ Create the wizard page. """

        details = Details(color=self.color)
        details.on_trait_change(self._on_name_changed, 'name')

        return details.edit_traits(parent=parent, kind='subpanel').control

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait event handlers #################################################

    def _on_name_changed(self, new):
        """ Called when the name has been changed. """

        self.complete = len(new.strip()) > 0

        return


# Application entry point.
if __name__ == '__main__':
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    wizard = ChainedWizard(
        parent = None,
        title  = 'Chained wizard root.',
        pages  = [ SimpleWizardPage(id='foo', color='red') ]
    )

    next_wizard = SimpleWizard(
        parent = None,
        title  = 'Chained wizard child.',
        pages  = [
            SimpleWizardPage(id='bar', color='yellow'),
            SimpleWizardPage(id='baz', color='green')
        ]
    )

    wizard.next_wizard = next_wizard

    # Open the wizard.
    if wizard.open() == OK:
        print 'Wizard completed successfully'

    else:
        print 'Wizard cancelled'

    # Start the GUI event loop!
    gui.event_loop()

#### EOF ######################################################################
