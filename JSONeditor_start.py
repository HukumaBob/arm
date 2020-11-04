import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QLabel, QAction
import connectutils
from MyClasses import GetListDb, comboboxInput, ViewTree
import json
from collections import OrderedDict
#import JSONtreepickup
import maindescription


class MainDescription(QtWidgets.QDialog, maindescription.Ui_DialogMainDescription):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле setupdlg.py
        super().__init__()
        self.setupUi(self)
# class JSONtreepickup(QtWidgets.QDialog, JSONtreepickup.Ui_Dialog_json):
#     def __init__(self):
#         # Это здесь нужно для доступа к переменным, методам
#         # и т.д. в файле setupdlg.py
#         super().__init__()
#         self.setupUi(self)


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())

def parse_txt(text):
    stack = []
    txt = []
    strng = ''
    flag = False
    for char in text:
        if char == '<':
            flag = True
            strin = ''
            txt.append(strng)
        elif char == '>':
            flag = False
            strng = ''
            stack.append(strin)
        elif(flag):
            #stack peek
            #stack[-1].append(char)
            strin = strin + char
        else:
            strng = strng + char
    parsing_txt = [[],[]]
    parsing_txt[1].extend(stack)
    parsing_txt[0].extend(txt)
    return (parsing_txt)

def findallkeys(value, mainkey, strextr = None):
    try:
        tmp_lst = []
        return_txt = OrderedDict({})
        if isinstance(mainkey, str):
            tmp_lst.append(mainkey)
        else:
            tmp_lst = mainkey
        i = 0
        for substr in tmp_lst:
            if isinstance(value, dict):

                for key1 in sorted(value.keys()):
                    if key1 == substr:
                        str_prs = ''
                        if strextr:
                            str_prs = strextr[i]
                            i = i + 1
                        stringExtract = parse_txt(value[key1])
                        html_str = OrderedDict({
                            "attribute": key1,
                            "list_of_values": {},
                            "list_of_continues": {},
                            "string_parse": str_prs
                        })
                        list_of_values = OrderedDict({})
                        list_of_continues = OrderedDict({})

                        if isinstance(value[key1], str):
                            if len(stringExtract) > 0:
                                #print(stringExtract[0])
                                return (findallkeys(value, stringExtract[1], stringExtract[0]))

                        elif isinstance(value[key1], dict):
                                if(len(value[key1])):
                                    for key in sorted(value[key1].keys()):
                                        tmp =  value[key1][key]
                                        stringExtract = parse_txt(tmp)
                                        for extr in stringExtract[1]:
                                            tmp = tmp.replace('<' + extr + '>', '')
                                        list_of_values.update({key: tmp})
                                        list_of_continues.update({key: stringExtract[1]})
                                    html_str.update(list_of_values = list_of_values)
                                    html_str.update(list_of_continues=list_of_continues)

                return_txt.update({substr: html_str})

        return return_txt
    except Exception:
        print('problem in findallkeys foo')


dict_of_comboboxes = OrderedDict({})
labels_of_boxes = OrderedDict({})
layout_v_cboxes = OrderedDict({})
layout_h_cboxes = OrderedDict({})

class JSONeditor(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super(JSONeditor, self).__init__()
        uic.loadUi('JSONeditor.ui', self)
        connection = connectutils.getConnection()

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

    def add_cb(self, txt):
        sending_button = self.sender()
        self.append_combo(txt)

    def del_cb(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().close()
            layout.takeAt(i)

    def continue_cb(self, indx, lst):
        maintext = self.textEditDS
        text = maintext.toPlainText()
        if (text):
            for raw in lst[indx]:
                text = text.replace("'", "\"")
                text_in_tree = json.loads(text)
                raw_html = findallkeys(text_in_tree, raw)
                for key in raw_html:
                    self.append_combo(raw_html[key])

    def append_combo(self, txt):
        number_of_columns = 3
        box_name = txt.get('attribute')
        init_box_name = box_name + '_01'
        layout_v_name = "verticalLayout_" + box_name
        layout_h_name = "horizontalLayout_" + box_name + '_01'
        box_key_val = txt.get('list_of_values')
        box_key_cont = txt.get('list_of_continues')
        box_label_string_parse = txt.get('')
        box_number = box_name + '_01'
        try:
            if layout_h_cboxes[box_number]:
                layout_cboxes_keys = layout_h_cboxes.keys()
                cnt = 1
                for key in layout_cboxes_keys:
                    if key[0:-3] == box_name:
                        cnt = cnt + 1
                if cnt < 10:
                    str_cnt = str('_0' + str(cnt))
                else:
                    str_cnt = '_' + str(cnt)
                box_number = box_name + str_cnt

                layout_h_cboxes[box_number] = QtWidgets.QHBoxLayout(self.frame_one)
                layout_h_cboxes[box_number].setObjectName(layout_v_name)
        except Exception:
            box_label_string_parse = txt.get('string_parse')
            layout_h_cboxes[box_number] = QtWidgets.QHBoxLayout(self.frame_one)
            layout_h_cboxes[box_number].setObjectName(layout_v_name)

            layout_v_cboxes[box_name] = QtWidgets.QVBoxLayout(self.frame_one)
            layout_v_cboxes[box_name].setObjectName(layout_h_name)
            temp = list(layout_v_cboxes.items())
            res = [idx for idx, key in enumerate(temp) if key[0] == box_name]
            for k in res:
                col = k // number_of_columns
                row = k % number_of_columns
            self.gridLayout_2.setContentsMargins(0, 0, 100, 100)
            self.gridLayout_2.addLayout(layout_v_cboxes[box_name], col ,row)


        layout_v_cboxes[box_name].addLayout(layout_h_cboxes[box_number])



        dict_of_comboboxes[box_number] = QtWidgets.QComboBox(self.frame_one)
        dict_of_comboboxes[box_number].setObjectName(box_number)
        if box_number == init_box_name:
            labels_of_boxes[box_number] = QLabel()
            labels_of_boxes[box_number].setText(box_label_string_parse)
            layout_h_cboxes[box_number].addWidget(labels_of_boxes[box_number])
            box_name_add = box_number + "_plus"
            pushButtonAdd = QtWidgets.QPushButton(self.frame_one)
            pushButtonAdd.setObjectName(box_name_add)
            pushButtonAdd.setMaximumSize(QtCore.QSize(20, 20))
            pushButtonAdd.setText("+")
            layout_h_cboxes[box_number].addWidget(pushButtonAdd)
            pushButtonAdd.clicked.connect(lambda: self.add_cb(txt))
        else:
            box_name_delete = box_number + "_del"
            pushButtonDel = QtWidgets.QPushButton(self.frame_one)
            pushButtonDel.setObjectName(box_name_delete)
            pushButtonDel.setMaximumSize(QtCore.QSize(20, 20))
            pushButtonDel.setText("-")
            layout_h_cboxes[box_number].insertWidget(-1, pushButtonDel)
            pushButtonDel.clicked.connect(lambda: self.del_cb(layout_h_cboxes[box_number]))

        #self.horizontalLayout_4.insertWidget(0, dict_of_comboboxes[box_name])
        layout_h_cboxes[box_number].addWidget(dict_of_comboboxes[box_number])

        for key in box_key_val:
            dict_of_comboboxes[box_number].addItem(box_key_val[key], key)
        dict_of_comboboxes[box_number].currentIndexChanged.connect\
            (lambda: self.continue_cb(dict_of_comboboxes[box_number].itemData(dict_of_comboboxes[box_number].currentIndex()), box_key_cont))


    def add_ds(self, connection):
        try:
            ds_value = self.comboBox_ds.currentData()
            text = ''
            if(ds_value):
                with connection.cursor() as cursor:
                    sql = "SELECT json_depict FROM ds_anatomical_parts_manipulation_type WHERE " \
                          "id_ds_anatomical_parts_manipulation_type = '%s'" %(ds_value)
                    cursor.execute(sql)

                    for row in cursor:
                        text = row['json_depict']
                maintext = self.textEditDS
                if(text):
                    text = json.loads(text)

                    text1 = json.dumps(text, indent=4, sort_keys=True, ensure_ascii = False)
                    maintext.setPlainText(text1)
                    text1 = text1.replace("'", "\"")
                    text_in_tree = json.loads(text1)

                    tree_window = ViewTree(text_in_tree)
                    self.clearLayout(self.verticalLayout_3)
                    self.verticalLayout_3.addWidget(tree_window)
                    raw_html = findallkeys( text_in_tree, "dsc.txt.000.000")
                    for key in raw_html:
                        self.append_combo(raw_html[key])
                    tree_window.installEventFilter(self)
                    self.context_menu_1 = QAction(self.tr('Edit'), self)
                    self.context_menu_2 = QAction(self.tr('Delete'), self)
                    self.context_menu_1.triggered.connect(lambda: self.copy_action(tree_window))

        except Exception:
            print('problem in add_ds foo')

    def copy_action(self, wdj):
        # item = wdj.currentItem()
        # txt = ''
        # # while (item):
        # #     txt = item.text(0)
        # #     print(txt)
        #     #item = item.parent()
        # txt = item.child(0).text(0)
        # json_pickup = JSONtreepickup()
        # _translate = QtCore.QCoreApplication.translate
        # #txt = txt.split('.')[-1]
        # json_pickup.setWindowTitle(_translate("JSONtreepickup", txt))
        # json_pickup.lineEditAttribute.setText(_translate("JSONtreepickup", txt))
        # json_pickup.lineEditKey1.setText('hggjhghgjgjgjgjhg')
        # json_pickup.exec()

        try:
            item = tmpitem = wdj.currentItem()
            att = 0
            key = 0
            val = 0
            txt = ''
            while(tmpitem):
                txt = tmpitem.text(0).split('.')
                lengh = len(txt)
                if (lengh > 1 and txt[1] == 'dsc'):
                    print('description')
                elif (lengh > 1 and txt[1] == 'att'):
                    print('attribute')
                elif (lengh > 1 and txt[1] == 'val'):
                    print('key')
                elif (lengh > 1 and txt[1] == 'txt'):
                    print('text')
                else:
                    print('value')
                cnt = tmpitem.childCount()
                item = tmpitem
                tmpitem = tmpitem.parent()

            indx = 1
            while (cnt > indx):
                txt = item.child(indx).text(0)
                print(txt)
                print(indx)
                indx = indx + 1
            # txt = item.child(0).text(0)
            # json_pickup = JSONtreepickup()
            _translate = QtCore.QCoreApplication.translate
            txt = txt.split('.')[-1]
            size_object = QtWidgets.QDesktopWidget().screenGeometry(-1)
            maindesc = MainDescription()
            _translate = QtCore.QCoreApplication.translate
            maindesc.setWindowTitle(_translate("DialogMainDescription", txt))
            maindesc.move(0, 0)
            wwidth = size_object.width() / 2
            wheight = size_object.height() - 40
            maindesc.resize(wwidth, wheight)
            self.verticalLayout = QtWidgets.QVBoxLayout(maindesc)
            self.verticalLayout.setObjectName("verticalLayout")
            self.lineEdit_attribute = QtWidgets.QLineEdit(maindesc)
            self.lineEdit_attribute.setObjectName("lineEdit_icd10")
            self.lineEdit_attribute.setMaximumSize(QtCore.QSize(1000, 20))
            self.lineEdit_attribute.setPlaceholderText(_translate("DialogMainDescription", "attribute"))
            self.verticalLayout.addWidget(self.lineEdit_attribute)
            self.scrollArea = QtWidgets.QScrollArea(maindesc)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setObjectName("scrollArea")
            self.WidgetContents = QtWidgets.QWidget()
            self.scrollArea.setWidget(self.WidgetContents)
            self.verticalLayout.addWidget(self.scrollArea)
            self.WidgetContents.setObjectName("WidgetContents")
            self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.WidgetContents)
            self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_4.setObjectName("verticalLayout_4")
            self.buttonBoxMainDescriptionOk = QtWidgets.QDialogButtonBox(maindesc)
            self.buttonBoxMainDescriptionOk.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
            self.buttonBoxMainDescriptionOk.setCenterButtons(True)
            self.buttonBoxMainDescriptionOk.setObjectName("buttonBoxMainDescriptionOk")
            findings_attributes = {}
            for raw in range(15):
                    raw = 1000 + raw
                    id_val = str(raw)[-3:]
                    findings_attributes[raw] = QtWidgets.QGroupBox(self.WidgetContents)
                    findings_attributes[raw].setObjectName(id_val)
                    self.verticalLayout_4.addWidget(findings_attributes[raw])

                    findings_attributes[raw].setTitle(_translate("DialogMainDescription", id_val))
                    self.verticalLayout_2 = QtWidgets.QVBoxLayout(findings_attributes[raw])
                    self.verticalLayout_2.setObjectName("verticalLayout_2")
                    self.groupBoxDs = QtWidgets.QGroupBox(findings_attributes[raw])
                    self.groupBoxDs.setObjectName("groupBoxDs")
                    self.groupBoxDs.setMaximumSize(QtCore.QSize(16777215, 26))
                    self.verticalLayout_2.addWidget(self.groupBoxDs)
                    self.horisontalLayout = QtWidgets.QHBoxLayout(self.groupBoxDs)
                    self.horisontalLayout.setObjectName("horisontalLayout")
                    self.horisontalLayout.setContentsMargins(0, 0, 0, 0)
                    self.horisontalLayout.setSpacing(6)
                    self.lineEdit_key = QtWidgets.QLineEdit(self.groupBoxDs)
                    self.lineEdit_key.setObjectName("lineEdit_key")
                    self.lineEdit_key.setMaximumSize(QtCore.QSize(60, 20))
                    self.lineEdit_key.setText(id_val)
                    self.lineEdit_value = QtWidgets.QLineEdit(self.groupBoxDs)
                    self.lineEdit_value.setObjectName("lineEdit_value")
                    self.lineEdit_value.setMaximumSize(QtCore.QSize(1000, 20))
                    self.lineEdit_value.setPlaceholderText(_translate("DialogMainDescription", "value"))

                    self.pushButton_New = QtWidgets.QPushButton(self.groupBoxDs)
                    self.pushButton_New.setObjectName("pushButton_New")
                    self.pushButton_New.setText(_translate("DialogMainDescription", "New"))
                    self.pushButton_Delete = QtWidgets.QPushButton(self.groupBoxDs)
                    self.pushButton_Delete.setObjectName("pushButton_Delete")
                    self.pushButton_Delete.setText(_translate("DialogMainDescription", "Delete"))

                    self.horisontalLayout.addWidget(self.lineEdit_key)
                    self.horisontalLayout.addWidget(self.lineEdit_value)
                    self.horisontalLayout.addWidget(self.pushButton_New)
                    self.horisontalLayout.addWidget(self.pushButton_Delete)


            self.verticalLayout.addWidget(self.buttonBoxMainDescriptionOk)
        except Exception:
                print('problem in dlg_main_description foo')
        maindesc.exec_()


    def eventFilter(self, obj, event):
        if event.type() == QEvent.ContextMenu:
            menu = QtWidgets.QMenu(self)
            menu.addAction(self.context_menu_1)
            menu.addAction(self.context_menu_2)
            menu.exec_(event.globalPos())
            return True
        return False


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