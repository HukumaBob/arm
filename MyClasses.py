#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QCompleter, QComboBox, QTreeWidget, QTreeWidgetItem
#from PyQt5.QtWidgets import  QApplication, QTreeWidget, QTreeWidgetItem

class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

class GetListDb:
 def __init__(self, connection, tbl = None, idtbl = None, col = None):
     self.tbl = tbl
     self.idtbl = idtbl
     self.col = col
     self.sql = "SELECT %s, %s FROM %s" % (idtbl, col, tbl)
     self.connection = connection

 def getlist(self):
     self.outlist = [[], []]
     self.connection.ping()
     try:
         with self.connection.cursor() as cursor:
             cursor.execute(self.sql)
             for row in cursor:
                 self.outlist[0].append(row[self.idtbl])
                 self.outlist[1].append(row[self.col])

         return self.outlist
     except Exception:
         return [[''], ['problem in GetListDb class']]

class comboboxInput:
    def __init__(self, lstclass, wdj, crntind=1):
        try:
            cnt = 0
            lst = lstclass.getlist()
            ct = wdj.itemText(0)
            wdj.clear()
            wdj.addItem(ct, None)

            for raw in lst[0]:
                wdj.addItem(str(lst[1][cnt]), str(lst[0][cnt]))
                cnt = cnt + 1

            wdj.setCurrentIndex(crntind)

            item = wdj.model().item(0)
            item.setEnabled(False)
        except Exception:
            return None

class ViewTree(QTreeWidget):
    def __init__(self, value):
        super().__init__()
        def fill_item(item, value):
            def new_item(parent, text, val=None):
                child = QTreeWidgetItem([text])
                fill_item(child, val)
                parent.addChild(child)
                child.setExpanded(True)
            if value is None: return
            elif isinstance(value, dict):
                for key, val in sorted(value.items()):
                    new_item(item, str(key), val)
            elif isinstance(value, (list, tuple)):
                for val in value:
                    text = (str(val) if not isinstance(val, (dict, list, tuple))
                            else '[%s]' % type(val).__name__)
                    new_item(item, text, val)
            else:
                new_item(item, str(value))

        fill_item(self.invisibleRootItem(), value)
