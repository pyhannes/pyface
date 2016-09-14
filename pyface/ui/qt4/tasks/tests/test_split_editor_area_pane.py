""" Tests for the SplitEditorAreaPane class. """

import os
import tempfile
import unittest

from traits.api import HasTraits, Instance

from pyface.qt import QtCore, QtWidgets
from pyface.tasks.split_editor_area_pane import EditorAreaWidget, \
    SplitEditorAreaPane
from pyface.tasks.api import Editor, PaneItem, Splitter, Tabbed, Task, \
    TaskWindow
from pyface.util.guisupport import get_app_qt4
from pyface.ui.qt4.util.testing import event_loop


class ViewWithTabsEditor(Editor):
    """ Test editor, displaying a labels in tabs. """

    name = 'Test Editor'

    def create(self, parent):
        """ Create and set the toolkit-specific contents of the editor.
        """
        control = QtWidgets.QTabWidget()
        control.addTab(QtWidgets.QLabel('tab 1'), 'group 1')
        control.addTab(QtWidgets.QLabel('tab 2'), 'group 2')
        self.control = control

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the editor.
        """
        self.control = None


class SplitEditorAreaPaneTestTask(Task):
    """ A test task containing a SplitEditorAreaPane. """

    id = 'test_task'
    name = 'Test Task'

    editor_area = Instance(SplitEditorAreaPane, ())

    def create_central_pane(self):
        return self.editor_area


class TestEditorAreaWidget(unittest.TestCase):
    """ Tests for the SplitEditorAreaPane class. """

    def _setUp_split(self, parent=None):
        """ Sets up the root splitter for splitting. Returns this root.

        parent : parent of the returned root
        """
        root = EditorAreaWidget(editor_area=SplitEditorAreaPane(),
                                parent=parent)
        btn0 = QtWidgets.QPushButton('0')
        btn1 = QtWidgets.QPushButton('1')
        tabwidget = root.tabwidget()
        tabwidget.addTab(btn0, '0')
        tabwidget.addTab(btn1, '1')
        tabwidget.setCurrentIndex(1)

        return root

    def test_split(self):
        """ Does split function work correct?
        """
        # setup
        root = self._setUp_split()
        tabwidget = root.tabwidget()
        btn0 = tabwidget.widget(0)
        btn1 = tabwidget.widget(1)

        # perform
        root.split(orientation=QtCore.Qt.Horizontal)

        # test
        # do we get correct leftchild and rightchild?
        self.assertIsNotNone(root.leftchild)
        self.assertIsNotNone(root.rightchild)
        self.assertIsInstance(root.leftchild, EditorAreaWidget)
        self.assertIsInstance(root.rightchild, EditorAreaWidget)
        self.assertEquals(root.leftchild.count(), 1)
        self.assertEquals(root.rightchild.count(), 1)

        # are the tabwidgets laid out correctly?
        self.assertEquals(root.leftchild.tabwidget(), tabwidget)
        self.assertIsNotNone(root.rightchild.tabwidget().empty_widget)

        # are the contents of the left tabwidget correct?
        self.assertEquals(root.leftchild.tabwidget().count(), 2)
        self.assertEquals(root.leftchild.tabwidget().widget(0), btn0)
        self.assertEquals(root.leftchild.tabwidget().widget(1), btn1)
        self.assertEquals(root.leftchild.tabwidget().currentWidget(), btn1)

        # does the right tabwidget contain nothing but the empty widget?
        self.assertEquals(root.rightchild.tabwidget().count(), 1)
        self.assertEquals(root.rightchild.tabwidget().widget(0),
                          root.rightchild.tabwidget().empty_widget)

        # do we have an equally sized split?
        self.assertEquals(root.leftchild.width(), root.rightchild.width())

        # is the rightchild active?
        self.assertEquals(root.editor_area.active_tabwidget,
                          root.rightchild.tabwidget())

    def _setUp_collapse(self, parent=None):
        """ Creates a root, its leftchild and rightchild, so that collapse can
        be tested on one of the children.

        Returns the root, leftchild and rightchild of such layout.

        parent : parent of the returned root
        """
        # setup leftchild
        left = EditorAreaWidget(editor_area=SplitEditorAreaPane(), parent=None)
        btn0 = QtWidgets.QPushButton('btn0')
        btn1 = QtWidgets.QPushButton('btn1')
        tabwidget = left.tabwidget()
        tabwidget.addTab(btn0, '0')
        tabwidget.addTab(btn1, '1')
        tabwidget.setCurrentIndex(1)

        # setup rightchild
        right = EditorAreaWidget(editor_area=left.editor_area, parent=None)
        btn2 = QtWidgets.QPushButton('btn2')
        btn3 = QtWidgets.QPushButton('btn3')
        tabwidget = right.tabwidget()
        tabwidget.addTab(btn2, '2')
        tabwidget.addTab(btn3, '3')
        tabwidget.setCurrentIndex(0)

        # setup root
        root = EditorAreaWidget(editor_area=left.editor_area, parent=parent)
        tabwidget = root.tabwidget()
        tabwidget.setParent(None)
        root.addWidget(left)
        root.addWidget(right)
        root.leftchild = left
        root.rightchild = right

        return root, left, right

    def test_collapse_nonempty(self):
        """ Test for collapse function when the source of collapse is not an
        empty  tabwidget. This would result in a new tabwidget which merges
        the tabs of the  collapsing tabwidgets.
        """
        # setup root
        root, left, right = self._setUp_collapse()
        btn0 = left.tabwidget().widget(0)
        btn1 = left.tabwidget().widget(1)
        btn2 = right.tabwidget().widget(0)
        btn3 = right.tabwidget().widget(1)

        # perform collapse on rightchild
        root.rightchild.collapse()

        # test
        # has the root now become the leaf?
        self.assertEquals(root.count(), 1)
        self.assertIsInstance(root.widget(0), QtWidgets.QTabWidget)

        # how does the combined list look?
        self.assertEquals(root.tabwidget().count(), 4)
        self.assertEquals(root.tabwidget().currentWidget(), btn2)

    def test_collapse_empty(self):
        """ Test for collapse function when the collapse origin is an empty
        tabwidget. It's sibling can have an arbitrary layout and the result
        would be such that this layout is transferred to the parent.
        """
        # setup
        root = EditorAreaWidget(editor_area=SplitEditorAreaPane(), parent=None)
        tabwidget = root.tabwidget()
        tabwidget.setParent(None)
        left, left_left, left_right = self._setUp_collapse(parent=root)
        right = EditorAreaWidget(editor_area=root.editor_area, parent=root)
        root.leftchild = left
        root.rightchild = right

        # perform collapse on leftchild
        right.collapse()

        # test
        # is the layout of root now same as left?
        self.assertEquals(root.count(), 2)
        self.assertEquals(root.leftchild, left_left)
        self.assertEquals(root.rightchild, left_right)

        # are the contents of left_left and left_right preserved
        self.assertEquals(root.leftchild.tabwidget().count(), 2)
        self.assertEquals(root.rightchild.tabwidget().count(), 2)
        self.assertEquals(root.leftchild.tabwidget().currentIndex(), 1)
        self.assertEquals(root.rightchild.tabwidget().currentIndex(), 0)

        # what is the current active_tabwidget?
        self.assertEquals(root.editor_area.active_tabwidget,
                          root.leftchild.tabwidget())

    def test_persistence(self):
        """ Tests whether get_layout/set_layout work correctly by setting a
        given layout and getting back the obtained layout.
        """
        # setup the test layout - one horizontal split and one vertical split
        # on the rightchild of horizontal split, where the top tabwidget of
        # the vertical split is empty.
        layout = Splitter(
            Tabbed(PaneItem(id=0, width=600, height=600),
                   active_tab=0),
            Splitter(Tabbed(PaneItem(id=-1, width=600, height=300),
                            active_tab=0),
                     Tabbed(PaneItem(id=1, width=600, height=300),
                            PaneItem(id=2, width=600, height=300),
                            active_tab=0),
                     orientation='vertical'),
            orientation='horizontal')
        # a total of 3 files are needed to give this layout - one on the
        # leftchild of horizontal split, and the other two on the bottom
        # tabwidget of the rightchild's vertical split
        file0 = open(os.path.join(tempfile.gettempdir(), 'file0'), 'w+b')
        file1 = open(os.path.join(tempfile.gettempdir(), 'file1'), 'w+b')
        file2 = open(os.path.join(tempfile.gettempdir(), 'file2'), 'w+b')

        # adding the editors
        editor_area = SplitEditorAreaPane()
        editor_area.create(parent=None)
        editor_area.add_editor(Editor(obj=file0, tooltip="test_tooltip0"))
        editor_area.add_editor(Editor(obj=file1, tooltip="test_tooltip1"))
        editor_area.add_editor(Editor(obj=file2, tooltip="test_tooltip2"))

        ######## test tooltips #############

        self.assertEquals(editor_area.active_tabwidget.tabToolTip(0),
                          "test_tooltip0")
        self.assertEquals(editor_area.active_tabwidget.tabToolTip(1),
                          "test_tooltip1")
        self.assertEquals(editor_area.active_tabwidget.tabToolTip(2),
                          "test_tooltip2")

        ######## test set_layout #############

        # set the layout
        editor_area.set_layout(layout)

        # file0 goes to left pane?
        left = editor_area.control.leftchild
        editor = editor_area._get_editor(left.tabwidget().widget(0))
        self.assertEquals(editor.obj, file0)

        # right pane is a splitter made of two panes?
        right = editor_area.control.rightchild
        self.assertFalse(right.is_leaf())

        # right pane is vertical splitter?
        self.assertEquals(right.orientation(), QtCore.Qt.Vertical)

        # top pane of this vertical split is empty?
        right_top = right.leftchild
        self.assertTrue(right_top.is_empty())

        # bottom pane is not empty?
        right_bottom = right.rightchild
        self.assertFalse(right_bottom.is_empty())

        # file1 goes first on bottom pane?
        editor = editor_area._get_editor(right_bottom.tabwidget().widget(0))
        self.assertEquals(editor.obj, file1)

        # file2 goes second on bottom pane?
        editor = editor_area._get_editor(right_bottom.tabwidget().widget(1))
        self.assertEquals(editor.obj, file2)

        # file1 tab is active?
        self.assertEquals(right_bottom.tabwidget().currentIndex(), 0)

        ######### test get_layout #############

        # obtain layout
        layout_new = editor_area.get_layout()

        # is the top level a horizontal splitter?
        self.assertIsInstance(layout_new, Splitter)
        self.assertEquals(layout_new.orientation, 'horizontal')

        # tests on left child
        left = layout_new.items[0]
        self.assertIsInstance(left, Tabbed)
        self.assertEquals(left.items[0].id, 0)

        # tests on right child
        right = layout_new.items[1]
        self.assertIsInstance(right, Splitter)
        self.assertEquals(right.orientation, 'vertical')

        # tests on top pane of right child
        right_top = right.items[0]
        self.assertIsInstance(right_top, Tabbed)
        self.assertEquals(right_top.items[0].id, -1)

        # tests on bottom pane of right child
        right_bottom = right.items[1]
        self.assertIsInstance(right_bottom, Tabbed)
        self.assertEquals(right_bottom.items[0].id, 1)
        self.assertEquals(right_bottom.items[1].id, 2)

    def test_active_tabwidget_after_editor_containing_tabs_gets_focus(self):
        # Regression test: if an editor contains tabs, a change in focus
        # sets the editor area pane `active_tabwidget` to one of those tabs,
        # rather than the editor's tab, after certain operations (e.g.,
        # navigating the editor tabs using keyboard shortcuts).

        window = TaskWindow()

        task = SplitEditorAreaPaneTestTask()
        editor_area = task.editor_area
        window.add_task(task)

        # Show the window.
        with event_loop():
            window.open()

        with event_loop():
            app = get_app_qt4()
            app.setActiveWindow(window.control)

        # Add and activate an editor which contains tabs.
        editor = ViewWithTabsEditor()
        with event_loop():
            editor_area.add_editor(editor)
        with event_loop():
            editor_area.activate_editor(editor)

        # Check that the active tabwidget is the right one.
        self.assertIs(editor_area.active_tabwidget,
                      editor_area.control.tabwidget())

        with event_loop():
            window.close()

    def test_active_editor_after_focus_change(self):
        window = TaskWindow(size=(800, 600))

        task = SplitEditorAreaPaneTestTask()
        editor_area = task.editor_area
        window.add_task(task)

        # Show the window.
        with event_loop():
            window.open()

        with event_loop():
            app = get_app_qt4()
            app.setActiveWindow(window.control)

        # Add and activate an editor which contains tabs.
        left_editor = ViewWithTabsEditor()
        right_editor = ViewWithTabsEditor()

        with event_loop():
            editor_area.add_editor(left_editor)
        with event_loop():
            editor_area.control.split(orientation=QtCore.Qt.Horizontal)
        with event_loop():
            editor_area.add_editor(right_editor)

        editor_area.activate_editor(right_editor)
        self.assertEqual(editor_area.active_editor, right_editor)

        with event_loop():
            left_editor.control.setFocus()

        self.assertIsNotNone(editor_area.active_editor)
        self.assertEqual(editor_area.active_editor, left_editor)

        with event_loop():
            window.close()

if __name__ == '__main__':
    unittest.main()
