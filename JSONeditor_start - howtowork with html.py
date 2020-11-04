import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem, QTreeWidgetItem, QMessageBox, QAction, QApplication
from PyQt5 import QtWebEngineWidgets #Don't touch, I don't know why, but it don't working without that...
import connectutils
from MyClasses import GetListDb, comboboxInput, ViewTree
import json
import re



def findallkeys(value, mainkey):
    try:
        if isinstance(value, dict):
            for key1 in sorted(value.keys()):
                if key1 == mainkey:
                    if isinstance(value[key1], str):
                        stringExtract = re.findall(r'\<([^()]+)\>', value[key1])
                        #print(stringExtract)
                        for substr in stringExtract:
                           return (findallkeys(value, substr))

                    elif isinstance(value[key1], dict):
                            if(len(value[key1])):
                                #comboBox_ds = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
                                #comboBox_ds.setObjectName(key1)
                                html_str = '<select onchange="print(1111111)" name="' + key1 + '">'
                                for key in sorted(value[key1].keys()):
                                    tmp =  value[key1][key]
                                    stringExtract = re.findall(r'\<([^()]+)\>', tmp)

                                    html_str = html_str + '<option value="' + key + '">'
                                    for extr in stringExtract:
                                        tmp = tmp.replace('<' + extr + '>', '')
                                    html_str = html_str + tmp + '</option>'
                                html_str = html_str + '</select>'
                                #print(html_str)
                                return html_str
    except Exception:
        print('problem in findallkeys foo')



class JSONeditor(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super(JSONeditor, self).__init__()
        uic.loadUi('JSONeditor.ui', self)
        connection = connectutils.getConnection()
        my_web = self.textEdit_2
        raw_html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">' \
                   '<html><head><meta name="qrichtext" content="1" />' \
                   '<style type="text/css">' \
                   'p, li { white-space: pre-wrap; }' \
                   '</style></head><body style=" font-family:"MS Shell Dlg 2"; font-size:8.25pt; font-weight:400; font-style:normal;">' \
                   '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">'\
                   '<p></p>'\
                   '</p></body></html>'
        my_web.setHtml(raw_html)
        my_web.show()
        bx = GetListDb(connection,'manipulation_type', 'id_manipulation_type', 'manipulation')
        manip = self.comboBox_manipulation
        comboboxInput(bx, manip, 1)
        sel = "SELECT  anatomical_parts.id_anatomical_parts AS id_anatomical_parts,  anatomical_parts.anatomical_parts_la AS anatomical_parts_la " \
              "FROM manipulation_type_anatomical_parts  INNER JOIN anatomical_parts    " \
              "ON manipulation_type_anatomical_parts.id_anatomical_parts = anatomical_parts.id_anatomical_parts " \
              "WHERE manipulation_type_anatomical_parts.id_manipulation_type = '%s'"
        self.comboBox_manipulation.currentIndexChanged.connect \
            (lambda: self.change_other_box(connection, self.comboBox_anatomical_part, "id_anatomical_parts", "anatomical_parts_la", "anatomical_parts", sel))


        self.comboBox_anatomical_part.currentIndexChanged.connect \
            (lambda: self.change_ds_box(connection, self.comboBox_ds, "id_ds",
                                           "ds", "ds_anatomical_parts_manipulation_type"))

        self.comboBox_ds.currentIndexChanged.connect(lambda :self.add_ds(connection))


        self.show()

    def add_ds(self, connection):
        ds_value = self.comboBox_ds.currentData()
        text = ''
        if(ds_value):
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT json_depict FROM ds_anatomical_parts_manipulation_type WHERE " \
                          "id_ds_anatomical_parts_manipulation_type = '%s'" %(ds_value)
                    cursor.execute(sql)

                    for row in cursor:
                        text = row['json_depict']
            except Exception:
                print('problem in add_ds foo')
            maintext = self.textEditDS
            if(text):
                text = json.loads(text)

                text1 = json.dumps(text, indent=4, sort_keys=True, ensure_ascii = False)
                maintext.setPlainText(text1)
                text1 = text1.replace("'", "\"")
                text_in_tree = json.loads(text1)

                window = ViewTree(text_in_tree)
                self.clearLayout(self.verticalLayout_3)
                self.verticalLayout_3.addWidget(window)
                raw_html = findallkeys( text_in_tree, "mainstr")
                my_web = self.textEdit_2
                my_web.setHtml(raw_html)
                my_web.show()





    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def change_ds_box(self, connection, wdj, idtbl, col, tbl):
        if (idtbl):
            bx = GetListDb(connection, tbl, idtbl, col)
            sql = "SELECT  ds_anatomical_parts_manipulation_type.id_ds_anatomical_parts_manipulation_type AS id_ds,  " \
                     "ds_anatomical_parts_manipulation_type.ds_anatomical_parts_manipulation_type_ru AS ds,  " \
                     "ds_anatomical_parts_manipulation_type.id_anatomical_parts,  " \
                     "ds_anatomical_parts_manipulation_type.id_manipulation_type " \
                     "FROM ds_anatomical_parts_manipulation_type WHERE " \
                     "ds_anatomical_parts_manipulation_type.id_anatomical_parts = %s " \
                     "AND ds_anatomical_parts_manipulation_type.id_manipulation_type = '%s'" %(self.comboBox_anatomical_part.currentData(), self.comboBox_manipulation.currentData())
            bx.sql = sql
            combobox = comboboxInput(bx, wdj)

    def change_other_box(self, connection, wdj, idtbl, col, tbl, sel = False):
        if (idtbl):
            bx = GetListDb(connection, tbl, idtbl, col)
            send = self.sender().currentData()
            if(sel):
                bx.sql = sel % (send)
            else:
                bx.sql = "SELECT %s, %s FROM %s WHERE id_manipulation_type = '%s'" % (idtbl, col, tbl, send)
            combobox = comboboxInput(bx, wdj)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = JSONeditor()
    sys.exit(app.exec_())