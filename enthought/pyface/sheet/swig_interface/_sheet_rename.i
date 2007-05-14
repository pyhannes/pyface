// A bunch of %rename directives generated by BuildRenamers in config.py
// in order to remove the wx prefix from all global scope names.

#ifndef BUILDING_RENAMERS


%rename(SHEET_VALUE_STRING)                  wxSHEET_VALUE_STRING;
%rename(SHEET_VALUE_BOOL)                    wxSHEET_VALUE_BOOL;
%rename(SHEET_VALUE_NUMBER)                  wxSHEET_VALUE_NUMBER;
%rename(SHEET_VALUE_FLOAT)                   wxSHEET_VALUE_FLOAT;
%rename(SHEET_VALUE_CHOICE)                  wxSHEET_VALUE_CHOICE;
%rename(SHEET_VALUE_TEXT)                    wxSHEET_VALUE_TEXT;
%rename(SHEET_VALUE_LONG)                    wxSHEET_VALUE_LONG;
%rename(SHEET_VALUE_CHOICEINT)               wxSHEET_VALUE_CHOICEINT;
%rename(SHEET_VALUE_DATETIME)                wxSHEET_VALUE_DATETIME;
%rename(SheetNoCellCoords)                   wxSheetNoCellCoords;
%rename(SheetNoCellRect)                     wxSheetNoCellRect;
%rename(SHEET_DEFAULT_NUMBER_ROWS)           wxSHEET_DEFAULT_NUMBER_ROWS;
%rename(SHEET_DEFAULT_NUMBER_COLS)           wxSHEET_DEFAULT_NUMBER_COLS;
%rename(SHEET_DEFAULT_ROW_HEIGHT)            wxSHEET_DEFAULT_ROW_HEIGHT;
%rename(SHEET_DEFAULT_COL_WIDTH)             wxSHEET_DEFAULT_COL_WIDTH;
%rename(SHEET_DEFAULT_COL_LABEL_HEIGHT)      wxSHEET_DEFAULT_COL_LABEL_HEIGHT;
%rename(SHEET_DEFAULT_ROW_LABEL_WIDTH)       wxSHEET_DEFAULT_ROW_LABEL_WIDTH;
%rename(SHEET_LABEL_EDGE_ZONE)               wxSHEET_LABEL_EDGE_ZONE;
%rename(SHEET_MIN_ROW_HEIGHT)                wxSHEET_MIN_ROW_HEIGHT;
%rename(SHEET_MIN_COL_WIDTH)                 wxSHEET_MIN_COL_WIDTH;
%rename(SHEET_DEFAULT_SCROLLBAR_WIDTH)       wxSHEET_DEFAULT_SCROLLBAR_WIDTH;
%rename(SheetCellRenderer)                   wxSheetCellRenderer;
%rename(PySheetCellRenderer)                 wxPySheetCellRenderer;
%rename(SheetCellStringRenderer)             wxSheetCellStringRenderer;
%rename(SheetCellNumberRenderer)             wxSheetCellNumberRenderer;
%rename(SheetCellFloatRenderer)              wxSheetCellFloatRenderer;
%rename(SheetCellDateTimeRenderer)           wxSheetCellDateTimeRenderer;
%rename(SheetCellEnumRenderer)               wxSheetCellEnumRenderer;
%rename(SheetCellAutoWrapStringRenderer)     wxSheetCellAutoWrapStringRenderer;
%rename(SheetCellEditor)                     wxSheetCellEditor;
%rename(PySheetCellEditor)                   wxPySheetCellEditor;
%rename(SheetCellTextEditor)                 wxSheetCellTextEditor;
%rename(SheetCellNumberEditor)               wxSheetCellNumberEditor;
%rename(SheetCellFloatEditor)                wxSheetCellFloatEditor;
%rename(SheetCellBoolEditor)                 wxSheetCellBoolEditor;
%rename(SheetCellChoiceEditor)               wxSheetCellChoiceEditor;
%rename(SheetCellEnumEditor)                 wxSheetCellEnumEditor;
%rename(SheetCellAutoWrapStringEditor)       wxSheetCellAutoWrapStringEditor;
%rename(SheetCellAttr)                       wxSheetCellAttr;
%rename(SheetCellAttrProvider)               wxSheetCellAttrProvider;
%rename(PySheetCellAttrProvider)             wxPySheetCellAttrProvider;
%rename(SheetTableBase)                      wxSheetTableBase;
%rename(PySheetTableBase)                    wxPySheetTableBase;
%rename(SheetStringTable)                    wxSheetStringTable;
%rename(SHEETTABLE_REQUEST_VIEW_GET_VALUES)  wxSHEETTABLE_REQUEST_VIEW_GET_VALUES;
%rename(SHEETTABLE_REQUEST_VIEW_SEND_VALUES)  wxSHEETTABLE_REQUEST_VIEW_SEND_VALUES;
%rename(SHEETTABLE_NOTIFY_ROWS_INSERTED)     wxSHEETTABLE_NOTIFY_ROWS_INSERTED;
%rename(SHEETTABLE_NOTIFY_ROWS_APPENDED)     wxSHEETTABLE_NOTIFY_ROWS_APPENDED;
%rename(SHEETTABLE_NOTIFY_ROWS_DELETED)      wxSHEETTABLE_NOTIFY_ROWS_DELETED;
%rename(SHEETTABLE_NOTIFY_COLS_INSERTED)     wxSHEETTABLE_NOTIFY_COLS_INSERTED;
%rename(SHEETTABLE_NOTIFY_COLS_APPENDED)     wxSHEETTABLE_NOTIFY_COLS_APPENDED;
%rename(SHEETTABLE_NOTIFY_COLS_DELETED)      wxSHEETTABLE_NOTIFY_COLS_DELETED;
%rename(SheetTableMessage)                   wxSheetTableMessage;
%rename(SheetCellCoords)                     wxSheetCellCoords;
%rename(SheetCoords)						 wxSheetCoords;
%rename(Sheet)                               wxSheet;
%rename(SheetEvent)                          wxSheetEvent;
%rename(SheetSizeEvent)                      wxSheetSizeEvent;
%rename(SheetRangeSelectEvent)               wxSheetRangeSelectEvent;
%rename(SheetEditorCreatedEvent)             wxSheetEditorCreatedEvent;
#endif
