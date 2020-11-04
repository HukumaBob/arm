import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QEvent,QDate, QTime, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem, QTreeWidgetItem, QMessageBox, QAction, QApplication
from lxml import etree
import random
import passport  # Это наш конвертированный файл дизайна
import connectutils
import adddialog
import maindescription
import setupdlg
from MyClasses import ExtendedComboBox



class NameAndPatronym:
    def __init__(self, sexpick = False):
        # Подключиться к базе данных.
        connection.ping()
        try:
            self.gender = True if sexpick else False
            with connection.cursor() as cursor:
                self.string_list = [[''], ['']]
                # SQL
                sql = "SELECT firstnames FROM firstnames WHERE sex =  %d" % (self.gender)
                # Выполнить команду запроса (Execute Query).
                cursor.execute(sql)
                #print("cursor.description: ", cursor.description)
                for row in cursor:
                    self.string_list[0].append(row["firstnames"])

                sql = "SELECT patronymic FROM patronymic WHERE sex =  %d" % (self.gender)
                # Выполнить команду запроса (Execute Query).
                cursor.execute(sql)
                #print("cursor.description: ", cursor.description)
                for row in cursor:
                    self.string_list[1].append(row["patronymic"])
        except Exception:
            print('problem in NameAndPatronym class')





class ChangeSex:  # Для чекбокса с выбором пола
    def __init__(self, wdj_check, wdj_fn, wdj_pn):
        try:
            self.check = wdj_check.currentData()
            self.strNames = NameAndPatronym(self.check).string_list
            wdj_fn.setMaxCount(0)
            wdj_fn.setMaxCount(len(self.strNames[0]))
            wdj_fn.addItems(self.strNames[0])
            wdj_pn.setMaxCount(0)
            wdj_pn.setMaxCount(len(self.strNames[1]))
            wdj_pn.addItems(self.strNames[1])
        except Exception:
            print('problem in ChangeSex class')

class GetListDb:
 def __init__(self, tbl = None, idtbl = None, col = None):
     self.tbl = tbl
     self.idtbl = idtbl
     self.col = col
     self.sql = "SELECT %s, %s FROM %s" % (idtbl, col, tbl)

 def getlist(self):
     self.outlist = [[], []]
     connection.ping()
     try:
         with connection.cursor() as cursor:
             cursor.execute(self.sql)
             for row in cursor:
                 self.outlist[0].append(row[self.idtbl])
                 self.outlist[1].append(row[self.col])
         return self.outlist
     except Exception:
         return [[''], ['problem in GetListDb class']]

class InsertToTable:
    def __init__(self, tbl = None, idtbl = None, col = None):
         self.tbl = tbl
         self.idtbl = idtbl
         self.col = col
         self.sql = "INSERT INTO %s VALUES (%s)" % (tbl, col)

    def insert_value(self):
         self.outlist = [[], []]
         connection.ping()
         try:
             with connection.cursor() as cursor:
                 cursor.execute(self.sql)
                 for row in cursor:
                     self.outlist[0].append(row[self.idtbl])
                     self.outlist[1].append(row[self.col])
             return self.outlist
         except Exception:
             return [[''], ['problem in InsertToTable class']]

class AddDlg(QtWidgets.QDialog, adddialog.Ui_DialogAdd):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле setupdlg.py
        super().__init__()
        self.setupUi(self)

class MainDescription(QtWidgets.QDialog, maindescription.Ui_DialogMainDescription):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле setupdlg.py
        super().__init__()
        self.setupUi(self)


class SetupDlg(QtWidgets.QDialog, setupdlg.Ui_FormSetup):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле setupdlg.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        gb = self.comboBoxGender
        gb.addItem(QIcon("ico/female.png"), "Female", False)
        gb.addItem(QIcon("ico/male.png"), "Male", True)
        self.sex = self.comboBoxGender.currentData()
        tempstr = NameAndPatronym().string_list
        fn = self.comboBoxFirstName
        fn.addItems(tempstr[0])
        pn = self.comboBoxPatronimicName
        pn.addItems(tempstr[1])
        gb.currentIndexChanged.connect(lambda: ChangeSex(gb, fn, pn))
        self.comboBoxPrefix.currentIndexChanged.connect(self.stuff)
        self.lineEditSurname.textChanged.connect(self.stuff)
        self.tableWidgetPersonality.hideColumn(0)
        self.tableWidgetPersonality.setColumnWidth(2,50)
        self.tableWidgetPersonality.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidgetPersonality.horizontalHeader().setStretchLastSection(True)
        self.stuff()
        bx = GetListDb('specialization', 'id_specialization', 'specialization')
        self.cb_input(bx, self.comboBoxSpecialization, 0)

        bx = GetListDb('degree', 'id_degree', 'degree')
        self.cb_input(bx, self.comboBoxDegree, 0)

        bx = GetListDb('regions', 'id_regions', 'regions_name')
        self.cb_input(bx, self.comboBoxRegion, 0)
        self.comboBoxRegion.currentIndexChanged.connect(self.regchange)

        bx = GetListDb('reestrmo', 'id_reestrmo', 'hospital')
        bx.sql = "SELECT id_reestrmo, CONCAT(short_name,' - ',address_mo) AS hospital FROM reestrmo"
        self.cb_input(bx, self.comboBoxHospital, 0)

    def regchange(self):
        where = self.comboBoxRegion.currentIndex()
        if(where):
            where = self.comboBoxRegion.currentText()
            bx = GetListDb('reestrmo', 'id_reestrmo', 'hospital')
            bx.sql = "SELECT id_reestrmo, CONCAT(short_name,' - ',address_mo) " \
                     "AS hospital FROM reestrmo WHERE region LIKE '%" + where + "%' GROUP BY code_mo"

            self.cb_input(bx, self.comboBoxHospital, 0)
    def cb_input(self, lstclass, wdj, crntind = 1):
        cnt = 0
        lst = lstclass.getlist()
        #wdj.setStyleSheet("background:#000000")
        ct = wdj.itemText(0)
        wdj.clear()
        wdj.addItem(ct, None)
        for raw in lst[0]:
            wdj.addItem(lst[1][cnt], lst[0][cnt])
            cnt = cnt + 1
        wdj.setCurrentIndex(crntind)
        item = wdj.model().item(0)
        #item.setData(None, QtCore.Qt.ForegroundRole)
        #item.setForeground(QtGui.QColor('grey'))
        item.setEnabled(False)

    def stuff(self):
        pref = self.comboBoxPrefix.currentText()
        surname = self.lineEditSurname.text()+'%'

        if(not self.comboBoxPrefix.currentIndex()):
            pref = '%'
        connection.ping()
        try:
            with connection.cursor() as cursor:
                # SQL
                self.sql = "SELECT id_personal, CONCAT(surname,' ', " \
                      "firstname,' ', patronymic,', ', pref,', ', speciality,', ', " \
                      "from_hospital) AS pers FROM personal WHERE pref LIKE '%s' AND surname LIKE '%s' ORDER BY surname DESC" %(pref, surname)

                cursor.execute(self.sql)
                table = self.tableWidgetPersonality
                combo = QtWidgets.QComboBox()
                table.setRowCount(0)
                for row in cursor:
                    rowPosition = table.rowCount()
                    table.insertRow(rowPosition)
                    table.setItem(rowPosition, 0, QTableWidgetItem(str(row['id_personal'])))
                    table.setItem(rowPosition, 1, QTableWidgetItem(row['pers']))
                    combo = QtWidgets.QComboBox()
                    combo.addItem('...')
                    combo.addItem(QIcon("ico/edit.png"), "Edit", str(row['id_personal']))
                    combo.addItem(QIcon("ico/delete.png"), "Delete", str(row['id_personal']))
                    table.setCellWidget(rowPosition, 2, combo)


        except Exception:
            print('problem in stuff foo')
        finally:
            pass


class PassportApp(QtWidgets.QWidget, passport.Ui_FormPassport):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        gb = self.comboBoxGender
        gb.addItem(QIcon("ico/female.png"), "Female", False)
        gb.addItem(QIcon("ico/male.png"), "Male", True)
        self.sex = gb.currentData()
        gb.currentIndexChanged.connect(lambda: ChangeSex(gb, fn, pn))
        self.comboBoxLang.addItem(QIcon("ico/en.png"), "English", '')
        self.comboBoxLang.addItem(QIcon("ico/ru.png"), "Русский", 'ru_RU')
        self.comboBoxLang.activated[str].connect(self.lang_changed)
        self.lineEditSurname.editingFinished.connect(self.names_input)
        self.tempstr = NameAndPatronym().string_list
        fn = self.comboBoxFirstName
        fn.addItems(self.tempstr[0])
        pn = self.comboBoxPatronimicName
        pn.addItems(self.tempstr[1])
        fn.editTextChanged.connect(self.names_input)
        pn.currentTextChanged.connect(self.names_input)


        self.connectwbase("SELECT regions_name_full, regions_code FROM regions")
        self.comboBoxRegion.activated[str].connect(self.on_combobox_changed)
        self.comboBoxAdress.editingFinished.connect(self.lineeditstreetchanged)
        self.trans = QtCore.QTranslator(self)
        self.retranslateUi(self)

        self.dateEditDateOfBirth.dateChanged.connect(self.age)

        self.treeWidgetPatientMatch.hideColumn(0)
        self.treeWidgetPatientMatch.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.treeWidgetPatientMatch.itemClicked.connect(self.tree_clicked)
        # self.treeWidgetPatientMatch.header().setStretchLastSection(False)
        # self.treeWidgetPatientMatch.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.tableWidgetPreviousPatients.hideColumn(0)
        self.tableWidgetPreviousPatients.hideColumn(6)
        # self.tableWidgetPreviousPatients.setColumnWidth(1,200)
        self.tableWidgetPreviousPatients.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidgetPreviousPatients.horizontalHeader().setStretchLastSection(True)

        self.pushButton_Edit.clicked.connect(self.editbutton)
        self.pushButtonNew.clicked.connect(self.new_record)
        self.pushButtonOk.clicked.connect(self.insert_passto_table)
        self.pushButton_Delete.clicked.connect(self.delete_passfrom_table)


        self.prevpatients()

        self.tableWidgetPreviousPatients.installEventFilter(self)
        self.context_menu_1 = QAction(self.tr('Insert to passport'), self)
        self.context_menu_2 = QAction(self.tr('View document'), self)
        self.context_menu_3 = QAction(self.tr('Video'), self)
        self.context_menu_4 = QAction(self.tr('Photo'), self)
        self.context_menu_1.triggered.connect(self.copy_action)

        self.pushButtonReasons.clicked.connect\
            (lambda: self.add_dlg( 'id_reasons',
                                   'reasons', 'reasons', 'id_manipulation_type',
                                   self.comboBoxManipulation, self.comboBoxReason))

        self.pushButtonRecommendation.clicked.connect\
            (lambda: self.add_dlg( 'id_recommendation',
                                   'recommendation', 'recommendation', 'id_manipulation_type', self.comboBoxManipulation, self.comboBoxRecommendation))
        self.pushButtonOptions.clicked.connect(self.open_setup)
        self.pushButtonPreparation.clicked.connect\
            (lambda: self.add_dlg( 'id_preparation',
                                   'preparation', 'preparation', 'id_manipulation_type', self.comboBoxManipulation, self.comboBoxPreparation))
        self.pushButtonDevices.clicked.connect \
            (lambda: self.add_dlg('id_equipment',
                                  'equipment', 'equipment', None, None,
                                  self.comboBoxDevices))

        now = QDateTime.currentDateTime()
        self.dateTimeEditBegin.setDateTime(now)
        self.pushButtonDateTimeRefresh.clicked.connect(lambda :self.dateTimeEditBegin.setDateTime(QDateTime.currentDateTime()))



        bx = GetListDb('manipulation_type', 'id_manipulation_type', 'manipulation')
        self.cb_input(bx, self.comboBoxManipulation, 0)

        bx = GetListDb('manipulation_kind', 'id_manipulation_kind', 'manipulation_kind_rus')
        self.cb_input(bx, self.comboBoxManipulationType, 0)

        bx = GetListDb('finance', 'id_finance', 'finance')
        self.cb_input(bx, self.comboBoxMoney, 0)

        bx = GetListDb('last_manipulation', 'id_last_manipulation', 'last_manipulation')
        self.cb_input(bx, self.comboBoxLastTime, 0)

        bx = GetListDb('hospital_departments', 'id_hospital_departments', 'hospital_departments')
        self.cb_input(bx, self.comboBoxDept, 0)

        bx = GetListDb('anesthesia', 'id_anesthesia', 'anesthesia')
        self.cb_input(bx, self.comboBoxAnesthesia, 0)

        manip = self.comboBoxManipulation
        manip.currentTextChanged.connect\
            (lambda: self.change_other_box(self.comboBoxReason, 'id_reasons', 'reasons', 'reasons', manip.currentData()))
        manip.currentTextChanged.connect \
            (lambda: self.change_other_box(self.comboBoxRecommendation, 'id_recommendation', 'recommendation', 'recommendation',
                                           manip.currentData()))
        manip.currentTextChanged.connect \
            (lambda: self.change_other_box(self.comboBoxPreparation, 'id_preparation', 'preparation',
                                           'preparation',
                                           manip.currentData()))
        manip.currentTextChanged.connect \
            (lambda: self.change_other_box(self.comboBoxDevice, 'id_device', 'device',
                                           'device',
                                           manip.currentData()))

        fromdoctor = self.comboBoxFromDoctor
        fromhospital = self.comboBoxFromHospital
        bx = GetListDb('personal', 'id_personal', 'surname')
        self.cb_input(bx, fromdoctor, 0)
        fromdoctor.currentTextChanged.connect(lambda :self.set_text_and_value_in_cbox(fromhospital))

        bx = GetListDb('hospital_departments', 'id_hospital_departments', 'hospital_departments')
        self.cb_input(bx, self.comboBoxDept, 0)

        bx = GetListDb('reasons_for', 'id_reasons_for', 'reasons_for')
        self.cb_input(bx, self.comboBoxReasonFor, 0)

        bx = GetListDb('personal', 'id_personal', 'surname')
        bx.sql = "SELECT  personal.id_personal,  " \
                 "personal.surname FROM personal  INNER JOIN default_all ON personal.reestr = default_all.id_reestrmo " \
                 "WHERE personal.speciality LIKE '%эндоскоп%' AND personal.pref = 'doctor'"
        self.cb_input(bx, self.comboBoxDoctor, 0)

        bx.sql = "SELECT  personal.id_personal,  " \
                 "personal.surname FROM personal  INNER JOIN default_all ON personal.reestr = default_all.id_reestrmo " \
                 "WHERE personal.speciality LIKE '%эндоскоп%' AND personal.pref = 'doctor'"
        self.cb_input(bx, self.comboBoxAssistant, 0)

        bx.sql = "SELECT  personal.id_personal,  " \
                 "personal.surname FROM personal  INNER JOIN default_all ON personal.reestr = default_all.id_reestrmo " \
                 "WHERE personal.speciality LIKE '%эндоскоп%' AND personal.pref = 'nurse'"
        self.cb_input(bx, self.comboBoxNurse, 0)

        bx.sql = "SELECT  personal.id_personal,  " \
                 "personal.surname FROM personal  INNER JOIN default_all ON personal.reestr = default_all.id_reestrmo " \
                 "WHERE personal.speciality LIKE '%Анестезио%' AND personal.pref = 'doctor'"
        self.cb_input(bx, self.comboBoxAnesthesiologist, 0)

        bx = GetListDb('reestrmo', 'id_reestrmo', 'short_name')
        bx.sql = "SELECT reestrmo.id_reestrmo, reestrmo.short_name FROM default_all INNER JOIN reestrmo ON default_all.region = reestrmo.region"
        self.cb_input(bx, self.comboBoxFromHospital, 0)

        bx = GetListDb('reestrins', 'code_imo', 'short_name')
        bx.sql = "SELECT reestrins.code_imo, reestrins.short_name FROM default_all INNER JOIN reestrins ON default_all.region = reestrins.region"
        self.cb_input(bx, self.comboBoxInsuranceComp, 0)

        bx = GetListDb('limitations', 'id_limitations', 'limitations')
        self.cb_input(bx, self.comboBoxLimitation, 0)

        bx = GetListDb('followup', 'id_followup', 'followup')
        self.cb_input(bx, self.comboBoxFollowUp, 0)

        bx = GetListDb('equipment', 'id_equipment', 'equipment')
        self.cb_input(bx, self.comboBoxDevices, 0)

        txt_edit = self.textEditHeader
        root = etree.Element('html', version="5.0")
        etree.SubElement(root, 'head')
        body = etree.SubElement(root, 'body')
        caput_div = etree.SubElement(body, 'div', align="center")
        caput_div_font = etree.SubElement\
            (caput_div, 'font', style = "font-size:18px; font-family:'Courier New';color:blue")
        manipul = etree.SubElement(caput_div_font, 'nobr')
        self.comboBoxManipulation.currentIndexChanged.connect(lambda: self.cbox_to_xml(manipul, txt_edit))
        manipul_type = etree.SubElement(caput_div_font, 'nobr')
        self.comboBoxManipulationType.currentIndexChanged.connect(lambda: self.cbox_to_xml(manipul_type, txt_edit))
        preamble_div = etree.SubElement(body, 'div', align="left")
        preamble_div_font = etree.SubElement\
            (preamble_div, 'font', style = "font-size:14px; font-family:'Courier New'")

        nod = []
        for raw in range(15):
            nod.append(etree.SubElement(preamble_div_font, 'nobr'))
        self.comboBoxMoney.currentIndexChanged.connect\
            (lambda: self.cbox_to_xml(nod[0], txt_edit, 'Payment: ','.'))

        self.comboBoxDept.currentIndexChanged.connect\
            (lambda: self.cbox_to_xml(nod[1], txt_edit, 'Dept: ','.'))

        self.comboBoxReason.currentTextChanged.connect \
            (lambda: self.cbox_to_xml(nod[2], txt_edit, 'Reasons: '))

        self.comboBoxReasonFor.currentTextChanged.connect \
            (lambda: self.cbox_to_xml(nod[3], txt_edit, '(',').'))


        self.comboBoxFromDoctor.currentTextChanged.connect \
            (lambda: self.cbox_to_xml(nod[4], txt_edit, 'Sent: '))

        fromhospital.activated.connect \
            (lambda: self.cbox_to_xml(nod[5], txt_edit, '(', ').'))


        self.comboBoxPreparation.currentTextChanged.connect \
            (lambda: self.cbox_to_xml(nod[6], txt_edit, 'Preparation: ','.'))

        self.comboBoxAnesthesia.currentTextChanged.connect \
            (lambda: self.cbox_to_xml(nod[7], txt_edit, 'Anesthesia: ','.'))

        self.comboBoxLimitation.currentTextChanged.connect \
            (lambda: self.cbox_to_xml(nod[8], txt_edit, 'Limitations: ','.'))

        self.comboBoxRecommendation.currentTextChanged.connect \
            (lambda: self.cbox_to_xml(nod[9], txt_edit, 'Recommendations: ','.'))

        self.comboBoxFollowUp.currentTextChanged.connect \
            (lambda: self.cbox_to_xml(nod[10], txt_edit, 'Follow up: ', '.'))

        self.boxes_names_array = [self.comboBoxManipulation, self.comboBoxManipulationType, self.comboBoxMoney,
                                  self.comboBoxDept, self.comboBoxReason, self.comboBoxReasonFor,
                                  self.comboBoxFromDoctor, self.comboBoxPreparation, self.comboBoxAnesthesia,
                                  self.comboBoxAnesthesia,
                                  self.comboBoxLimitation, self.comboBoxInsuranceComp, self.comboBoxLastTime,
                                  self.comboBoxRecommendation, self.comboBoxFollowUp, self.comboBoxDoctor,
                                  self.comboBoxAssistant, self.comboBoxNurse, self.comboBoxAnesthesiologist,
                                  self.comboBoxDevices, self.comboBoxDevice, self.dateTimeEditBegin]
        #self.pushButtonSaveCase.clicked.connect(lambda :self.save_update_delete_case(1))
        self.pushButtonSaveCase.clicked.connect(lambda :self.create_update_case(self.boxes_names_array, 'cases'))

        self.pushButtonCopyCase.clicked.connect(self.prevpatients_update)

        self.lineEdit_id_case.setText('0')

        self.textBrowserSlogans.setHtml(str(self.slogans()))

        self.pushButtonNewRecord.clicked.connect(self.new_case)
        self.pushButtonDeleteCase.clicked.connect(self.case_delete)
        self.pushButtonDescription.clicked.connect(lambda :self.dlg_main_description())



    def dlg_main_description(self):
        caption = self.lineEditSurname.text() + ' ' + self.comboBoxFirstName.currentText() + ' ' + self.comboBoxPatronimicName.currentText()
        if(caption.replace(' ','') != ''):
            manip = self.comboBoxManipulation.currentData()
            if(manip != None):
                size_object = QtWidgets.QDesktopWidget().screenGeometry(-1)
                maindesc = MainDescription()
                _translate = QtCore.QCoreApplication.translate
                maindesc.setWindowTitle(_translate("DialogMainDescription", caption))
                maindesc.move(0, 0)
                wwidth = size_object.width()/2
                wheight = size_object.height()-40
                maindesc.resize(wwidth, wheight)
                self.verticalLayout = QtWidgets.QVBoxLayout(maindesc)
                self.verticalLayout.setObjectName("verticalLayout")
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
                self.buttonBoxMainDescriptionOk.setStandardButtons(
                    QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
                self.buttonBoxMainDescriptionOk.setCenterButtons(True)
                self.buttonBoxMainDescriptionOk.setObjectName("buttonBoxMainDescriptionOk")



                try:
                    connection.ping()
                    with connection.cursor() as cursor:
                        sql = "SELECT anatomical_parts.anatomical_parts_la AS anatomical_parts_la, " \
                              "anatomical_parts.id_anatomical_parts AS id_anatomical_parts " \
                              "FROM manipulation_type_anatomical_parts  INNER JOIN anatomical_parts  " \
                              "ON manipulation_type_anatomical_parts.id_anatomical_parts = anatomical_parts.id_anatomical_parts " \
                              "WHERE manipulation_type_anatomical_parts.id_manipulation_type = '%s'" %(manip)
                        cursor.execute(sql)
                        anatomical_parts = {}
                        anatomical_parts_cursor = cursor.fetchall()
                        for row in anatomical_parts_cursor:
                            anat_part = (row['anatomical_parts_la'])
                            id_anat = str(row['id_anatomical_parts'])
                            anatomical_parts[anat_part] = QtWidgets.QGroupBox(self.WidgetContents)
                            anatomical_parts[anat_part].setObjectName(id_anat)
                            self.verticalLayout_4.addWidget(anatomical_parts[anat_part])
                            anatomical_parts[anat_part].setTitle(_translate("DialogMainDescription", anat_part))
                            self.verticalLayout_2 = QtWidgets.QVBoxLayout(anatomical_parts[anat_part])
                            self.verticalLayout_2.setObjectName("verticalLayout_2")
                            self.groupBoxDs = QtWidgets.QGroupBox(anatomical_parts[anat_part])
                            self.groupBoxDs.setObjectName("groupBoxDs")
                            self.groupBoxDs.setMaximumSize(QtCore.QSize(16777215, 26))
                            self.verticalLayout_2.addWidget(self.groupBoxDs)


                            self.horisontalLayout = QtWidgets.QHBoxLayout(self.groupBoxDs)
                            self.horisontalLayout.setObjectName("horisontalLayout")
                            self.horisontalLayout.setContentsMargins(0, 0, 0, 0)
                            self.horisontalLayout.setSpacing(6)


                            self.comboBoxDs = ExtendedComboBox(self.groupBoxDs)
                            self.comboBoxDs.setObjectName("comboBoxDs")
                            self.comboBoxDsAppend = ExtendedComboBox(self.groupBoxDs)
                            self.comboBoxDs.setObjectName("comboBoxDsAppend")
                            self.lineEdit_icd10 = QtWidgets.QLineEdit(self.groupBoxDs)
                            self.lineEdit_icd10.setObjectName("lineEdit_icd10")
                            self.pushButton_New = QtWidgets.QPushButton(self.groupBoxDs)
                            self.pushButton_New.setObjectName("pushButton_New")
                            self.pushButton_New.setText(_translate("DialogMainDescription", "New"))
                            self.pushButton_Delete = QtWidgets.QPushButton(self.groupBoxDs)
                            self.pushButton_Delete.setObjectName("pushButton_Delete")
                            self.pushButton_Delete.setText(_translate("DialogMainDescription", "Delete"))
                            self.comboBoxDs.setMaximumSize(QtCore.QSize(16777215, 20))
                            self.lineEdit_icd10.setMaximumSize(QtCore.QSize(60, 20))

                            self.horisontalLayout.addWidget(self.comboBoxDs)
                            self.horisontalLayout.addWidget(self.comboBoxDsAppend)
                            self.horisontalLayout.addWidget(self.lineEdit_icd10)
                            self.horisontalLayout.addWidget(self.pushButton_New)
                            self.horisontalLayout.addWidget(self.pushButton_Delete)

                            self.lineEdit_icd10.setPlaceholderText(_translate("DialogMainDescription", "ICD 10"))
                            self.groupBox_ds_depict = QtWidgets.QGroupBox(anatomical_parts[anat_part])
                            self.groupBox_ds_depict.setTitle("")
                            self.groupBox_ds_depict.setObjectName("groupBox_ds_depict")
                            self.groupBox_ds_depict.setMinimumHeight(200)
                            self.verticalLayout_2.addWidget(self.groupBox_ds_depict)
                            bx = GetListDb(None, 'id_ds', 'ds')
                            bx.sql = "SELECT  ds_anatomical_parts_manipulation_type.id_ds_anatomical_parts_manipulation_type AS id_ds,  " \
                                  "ds_anatomical_parts_manipulation_type.ds_anatomical_parts_manipulation_type_ru AS ds,  " \
                                  "ds_anatomical_parts_manipulation_type.id_anatomical_parts,  " \
                                  "ds_anatomical_parts_manipulation_type.id_manipulation_type " \
                                  "FROM ds_anatomical_parts_manipulation_type WHERE " \
                                  "ds_anatomical_parts_manipulation_type.id_anatomical_parts = %s " \
                                  "AND ds_anatomical_parts_manipulation_type.id_manipulation_type = '%s'" %(id_anat, manip)

                            self.cb_input(bx, self.comboBoxDs, 0)
                        self.verticalLayout.addWidget(self.buttonBoxMainDescriptionOk)

                except Exception:
                    print('problem in dlg_main_description foo')
                maindesc.exec_()




    def new_c(self, wdj):
        wdj.setCurrentIndex(0)
        wdj.setStyleSheet("QComboBox { background-color: ; }")
    def new_case(self):
        self.lineEdit_id_case.setText('0')
        self.new_c(self.comboBoxManipulation)
        self.new_c(self.comboBoxManipulationType)
        self.new_c(self.comboBoxMoney)
        self.new_c(self.comboBoxDept)
        self.new_c(self.comboBoxReason)
        self.new_c(self.comboBoxReasonFor)
        self.new_c(self.comboBoxFromDoctor)
        self.new_c(self.comboBoxFromHospital)
        self.new_c(self.comboBoxPreparation)
        self.new_c(self.comboBoxAnesthesia)
        self.new_c(self.comboBoxLimitation)
        self.new_c(self.comboBoxInsuranceComp)
        self.new_c(self.comboBoxLastTime)
        self.new_c(self.comboBoxRecommendation)
        self.new_c(self.comboBoxFollowUp)
        self.new_c(self.comboBoxDoctor)
        self.new_c(self.comboBoxAssistant)
        self.new_c(self.comboBoxNurse)
        self.new_c(self.comboBoxAnesthesiologist)
        self.new_c(self.comboBoxDevices)
        self.new_c(self.comboBoxDevice)
        now = QDateTime.currentDateTime()
        self.dateTimeEditBegin.setDateTime(now)

    def slogans(self):
        try:
            self.tmp = 0
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) as cnt FROM slogans"
                cursor.execute(sql)
                for row in cursor:
                    self.tmp = random.randint(0, row['cnt'])
                    sql = "SELECT slogans FROM slogans WHERE id_slogans = '%d'" %(self.tmp)
                    cursor.execute(sql)
                    for row in cursor:
                        self.tmp ='<p style="font-size:14px; color:green; text-align: center">' + row['slogans'] + '</p>'

            return self.tmp
        except Exception:
            print('problem in slogans foo')

    def create_update_case(self,arr, prefix):
        try:
            id_case = int(self.lineEdit_id_case.text())
            id_passport = int(self.lineEdit_id_passport.text())
            flag = 'insert'
            connection.ping()
            if (id_passport and id_case == 0):
                with connection.cursor() as cursor:
                    sql = "INSERT INTO cases (id_passport) VALUES ('%d')" % (id_passport)
                    cursor.execute(sql)
                    connection.commit()
                    sql = "SELECT LAST_INSERT_ID() as last_id"
                    cursor.execute(sql)
                    for raw in cursor:
                        id_case = str(raw['last_id'])
                        self.lineEdit_id_case.setText(id_case)
            elif(id_passport and id_case):
                flag = 'update'
            self.insert_data_in_boxes(arr, prefix, id_case, flag)
            self.prevpatients_update(flag)
        except Exception:
            print('problem in create_update_case foo')

    def insert_data_in_boxes(self, arr, prefix, id_tbl, flag):
        try:
            with connection.cursor() as cursor:
                for raw in arr:
                    tbl = prefix +'_' + raw.accessibleName()
                    id_col = 'id_' + prefix
                    val_col = 'id_' + raw.accessibleName()
                    if(flag == 'update'):
                        sql = "DELETE FROM %s WHERE %s = '%s'" % (tbl, id_col, id_tbl)
                        cursor.execute(sql)
                        connection.commit()
                    if raw == self.dateTimeEditBegin:  # Костыль!!!!
                        valarr = raw.text().split(' ')  # datetime 11.14.2019 11:30 to mysql format 2019-11-14 11:30
                        dts = valarr[0].split('.')
                        val = dts[2] + '-' + dts[1] + '-' + dts[0] + ' ' + valarr[1]
                        sql = "INSERT INTO %s (%s, %s) VALUES ('%s', '%s')" % (
                            tbl, id_col, val_col, id_tbl, val)
                        cursor.execute(sql)
                        connection.commit()
                    else:
                        if(raw.currentData()):
                            val = str(raw.currentData()).split(', ')
                            for cur_dat in val:
                                sql = "INSERT INTO %s (%s, %s) VALUES ('%s', '%s')" % (
                                    tbl, id_col, val_col, id_tbl, cur_dat)
                                cursor.execute(sql)
                                connection.commit()
                            raw.setStyleSheet("QComboBox { background-color: hsl(180,25%,90%); }")
                    self.names_input()
        except Exception:
                    print('problem in insert_data_in_boxes foo')

    def case_delete(self):

        try:
            id_case = int(self.lineEdit_id_case.text())
            if(id_case):
                with connection.cursor() as cursor:
                    sql = "DELETE FROM cases WHERE id_cases = '%d'" % (id_case)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()
                    self.prevpatients_update('delete')
                    self.names_input()
        except Exception:
                    print('problem in case_delete foo')

    def case_select_and_insert_to_comboboxes(self):
        try:
            connection.ping()
            with connection.cursor() as cursor:
                for raw in self.boxes_names_array:
                    self.case_select(raw)
        except Exception:
            print('problem in case_select_and_insert_to_comboboxes foo')

    def case_select(self, wdj):
        try:
            with connection.cursor() as cursor:
                self.wdj_data = ''
                self.wdj_txt = ''
                i = 0
                id_case = self.lineEdit_id_case.text()
                id_tbl = 'id_' + wdj.accessibleName()
                tbl = 'cases_' + wdj.accessibleName()
                sql = "SELECT %s FROM %s WHERE id_cases = '%s' ORDER BY %s ASC" % (id_tbl, tbl,  id_case, id_tbl)
                cursor.execute(sql)
                wdj.setStyleSheet("QComboBox { background-color: ; }")
                if (wdj != self.dateTimeEditBegin):
                    wdj.setCurrentIndex(0)
                for raw in cursor:
                    if (wdj == self.dateTimeEditBegin):
                        dt = str(raw[id_tbl]).replace(' ', ':').replace('-', ':').split(':')
                        self.dateTimeEditBegin.setDateTime \
                            (QDateTime(int(dt[0]), int(dt[1]), int(dt[2]), int(dt[3]), int(dt[4])))
                    else:
                        if (cursor.rowcount == 1):
                            wdj.setCurrentIndex(wdj.findData(raw[id_tbl]))
                        elif (cursor.rowcount > 1):
                            i = i + 1
                            self.wdj_data = self.wdj_data + str(raw[id_tbl]) + ', '
                            try:
                                wdj.setCurrentIndex(wdj.findData(raw[id_tbl]))
                            finally:
                                self.wdj_txt = self.wdj_txt + wdj.currentText() + ', '
                            if (cursor.rowcount == i):
                                wdj.setCurrentIndex(0)
                                wdj.setItemData(0, self.wdj_data[:-2])
                                wdj.setCurrentText(self.wdj_txt[:-2])
        except Exception:
            print('problem in case_select foo')


    def prevpatupd(self, row):
        id_passport = self.lineEdit_id_passport.text()
        self.tableWidgetPreviousPatients.setItem(row, 0, QTableWidgetItem(id_passport))
        tmp = self.lineEditSurname.text() + ' ' + self.comboBoxFirstName.currentText() + ' ' + self.comboBoxPatronimicName.currentText()
        self.tableWidgetPreviousPatients.setItem(row, 1, QTableWidgetItem(tmp))
        tmp = self.dateEditDateOfBirth.text().split('.')
        tmp = tmp[2] + '-' + tmp[1] + '-' + tmp[0]
        self.tableWidgetPreviousPatients.setItem(row, 2, QTableWidgetItem(tmp))
        tmp = self.comboBoxManipulation.currentData()
        self.tableWidgetPreviousPatients.setItem(row, 3, QTableWidgetItem(tmp))
        tmp = self.dateTimeEditBegin.text().split(' ')
        tm = tmp[1]
        tmp = tmp[0].split('.')
        tmp = tmp[2] + '-' + tmp[1] + '-' + tmp[0] + ' ' + tm
        self.tableWidgetPreviousPatients.setItem(row, 4, QTableWidgetItem(tmp))
        tmp = self.comboBoxDoctor.currentText()
        self.tableWidgetPreviousPatients.setItem(row, 5, QTableWidgetItem(tmp))
        tmp = self.lineEdit_id_case.text()
        self.tableWidgetPreviousPatients.setItem(row, 6, QTableWidgetItem(tmp))

    def prevpatients_update(self, myflag):
        try:
            row = 0
            id_case = self.lineEdit_id_case.text()
            id_passport = self.lineEdit_id_passport.text()
            if(int(id_passport) and int(id_case)):
                if(myflag == 'insert'):
                    row = 0
                    self.tableWidgetPreviousPatients.insertRow(row)
                    self.prevpatupd(row)
                elif(myflag == 'update'):
                    tmps = self.tableWidgetPreviousPatients.findItems(id_case, QtCore.Qt.MatchExactly)
                    for tmp in tmps:
                        if(tmp.column() == 6): # If number of id_case will changed - change the figure also
                            row = tmp.row()
                    self.prevpatupd(row)
                elif (myflag == 'delete'):
                    tmps = self.tableWidgetPreviousPatients.findItems(id_case, QtCore.Qt.MatchExactly)
                    for tmp in tmps:
                        if (tmp.column() == 6):  # If number of id_case will changed - change the figure also
                            row = tmp.row()
                            self.tableWidgetPreviousPatients.removeRow(row)
                            self.new_case()
        except Exception:
            print('problem in prevpatients_update function')

    def cbox_to_xml(self, nod, txt_edit, prefx = '', postfix = ''):
        prefx = self.tr(prefx)
        send = self.sender()

        if(send.currentData()):
            nod.text = prefx + send.currentText() + postfix
            nod.set('id', str(send.currentData()))
        else:
            nod.text = ''
        while (not (nod.tag == 'html')):
            nod = nod.getparent()
            if(nod.tag == 'html'):
                break
        txt_edit.setHtml(etree.tostring(nod, pretty_print=True).decode("utf-8"))



    def set_text_and_value_in_cbox(self, recept_wdg):
        try:
            send = self.sender()
            self.sql = "SELECT reestr, from_hospital FROM personal WHERE id_personal = %d" % (send.currentData())
            with connection.cursor() as cursor:
                cursor.execute(self.sql)
                for row in cursor:
                    ind = recept_wdg.findData(row['reestr'])
                    recept_wdg.setCurrentIndex(ind)
                    recept_wdg.setCurrentText(row['from_hospital'])
        except Exception:
            print('problem in set_text_and_value_in_cbox foo')

    def change_other_box(self, wdj, idtbl, col, tbl, currdat):
        if(idtbl):
            bx = GetListDb(tbl, idtbl, col)
            bx.sql = "SELECT %s, %s FROM %s WHERE id_manipulation_type = '%s'" % (idtbl, col, tbl, currdat)
            self.cb_input(bx, wdj, 0)





    def cb_input(self, lstclass, wdj, crntind = 1):
        try:
            cnt = 0
            lst = lstclass.getlist()
            #wdj.setStyleSheet("background:#000000")
            ct = wdj.itemText(0)
            wdj.clear()
            wdj.addItem(ct, None)
            for raw in lst[0]:
                wdj.addItem(lst[1][cnt], lst[0][cnt])
                cnt = cnt + 1
            wdj.setCurrentIndex(crntind)
            item = wdj.model().item(0)
            #item.setData(None, QtCore.Qt.ForegroundRole)
            #item.setForeground(QtGui.QColor('grey'))
            item.setEnabled(False)
        except Exception:
            print('problem in cb_input foo')

    def add_table(self, sql_list, table):
        try:
                table.setRowCount(0)
                for row in sql_list:
                    rowPosition = table.rowCount()
                    table.insertRow(rowPosition)
                    table.setItem(rowPosition, 0, QTableWidgetItem(str(row['id_personal'])))
                    table.setItem(rowPosition, 1, QTableWidgetItem(row['pers']))
                    combo = QtWidgets.QComboBox()
                    combo.addItem('...')
                    combo.addItem(QIcon("ico/edit.png"), "Edit", str(row['id_personal']))
                    combo.addItem(QIcon("ico/delete.png"), "Delete", str(row['id_personal']))
                    table.setCellWidget(rowPosition, 2, combo)
                    # self.index = self.index + 1

        except Exception:
            print('problem in add_table foo')

    def add_dlg(self, col, idtbl, tbl, restr_condition = None, wdjt = None, cmbbox = None):
        self.conditions = ''
        if(restr_condition):
            self.restrictions = wdjt.currentData()
            self.conditions = 'WHERE ' + restr_condition + " = '" + str(self.restrictions) + "'"
        else:
            pass
        adddlg = AddDlg()
        _translate = QtCore.QCoreApplication.translate
        adddlg.setWindowTitle(_translate("DialogAdd", tbl))
        bx = GetListDb(idtbl, col, tbl)
        bx.sql = "SELECT %s, %s FROM %s %s" % (idtbl, col, tbl, self.conditions)

        table = adddlg.tableWidgetAdd
        table.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        table.hideColumn(0)
        # table.setColumnWidth(1, 5)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        table.setRowCount(0)
        lst = bx.getlist()
        for row in lst[0]:
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            table.setItem(rowPosition, 0, QTableWidgetItem(str(lst[0][rowPosition])))
            table.setItem(rowPosition, 1, QTableWidgetItem(str(lst[1][rowPosition])))
            #check = QtWidgets.QCheckBox()
            #table.setCellWidget(rowPosition, 1, check)
        okbtn = adddlg.buttonBoxDialogOk
        okbtn.accepted.connect(adddlg.accept)
        okbtn.rejected.connect(adddlg.reject)
        if adddlg.exec_():
            self.text = ''
            self.dat = ''
            for row in range(table.rowCount()):
                items = table.item(row, 1)
                dats = table.item(row, 0)
                if(items.isSelected()):
                    self.text = self.text + str(items.text()) + ', '
                    self.dat = self.dat + dats.text() + ', '

            cmbbox.setCurrentIndex(0) # Important - to the beginning of the list
            cmbbox.setItemData(0,self.dat[:-2])
            cmbbox.setCurrentText(self.text[:-2])
        #adddlg.show()

    def open_setup(self):
        setupdlg = SetupDlg()
        setupdlg.exec()
        #setupdlg.show()

    def open_dialog(self, ui_dialog):
        dialog = QtWidgets.QDialog()
        dialog.ui = ui_dialog()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def delete_passfrom_table(self):
        id_pass = self.lineEdit_id_passport.text()
        if(id_pass):
            reply = QMessageBox.question(self, 'Attention',
                                         "Are you sure?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                connection.ping()
                try:
                    with connection.cursor() as cursor:
                        sql = "DELETE FROM passport WHERE id_passport = %d" %(int(id_pass))
                        cursor.execute(sql)
                        connection.commit()
                        self.new_record()
                        self.prevpatients()
                except Exception:
                    print('problem in delete_passfrom_table function')


    def insert_passto_table(self):
        age = 10000
        if(self.lineEditAge.text() == ''):
            self.lineEditSurname.setFocus()
            QMessageBox.question(self, 'Attention',
                                 "Field of date of birth is empty. You have to fill it. ")
        elif (self.lineEditSurname.text() == ''):
            QMessageBox.question(self, 'Attention',
                                 "Field of surname is empty. You have to fill it. ")
            self.lineEditSurname.setFocus()
        elif(int(self.lineEditAge.text().split(' ')[0])>110):
                reply = QMessageBox.question(self, 'Attention',
                                     "The patient is too old. May be this is a mistake?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.lineEditSurname.setFocus()
                else:
                    self.mysql_insert_topass()
        else:
            self.mysql_insert_topass()

    def mysql_insert_topass(self):

        date_of_birth = self.dateEditDateOfBirth.text().split('.')
        date_of_birth = date_of_birth[2]+'-'+date_of_birth[1]+'-'+date_of_birth[0]
        surname = self.lineEditSurname.text()
        firstname = self.comboBoxFirstName.currentText()
        patronymic = self.comboBoxPatronimicName.currentText()
        address = self.comboBoxAdress.text()
        building = self.lineEditHouseRoom.text()
        phone = self.lineEditPhone.text()
        email = self.lineEditEmail.text()
        gender = -self.comboBoxGender.currentIndex()

        id_pass = int(self.lineEdit_id_passport.text())
        if(self.lineEditSurname.isEnabled()):
            if(not(id_pass)):
                connection.ping()
                try:
                    with connection.cursor() as cursor:
                        # SQL
                        sql = "INSERT INTO passport " \
                              "(date_of_birth, surname,firstname," \
                              "patronymic,address,building,phone,email,gender) VALUES " \
                              "('%s','%s','%s','%s','%s','%s','%s','%s',%d)"\
                              % (date_of_birth, surname,firstname,patronymic,address,building,phone,email,gender)
                        cursor.execute(sql)
                        connection.commit()
                        sql = "SELECT LAST_INSERT_ID() as last_id"
                        cursor.execute(sql)
                        # print(list(cursor)[0]['last_id'])
                        for raw in cursor:
                            self.lineEdit_id_passport.setText(str(raw['last_id']))
                            self.names_input()
                            self.fields_disable(True)
                            self.prevpatients()
                except Exception:
                    print('problem in insert_passto_table function')
            else:
                connection.ping()
                try:
                    with connection.cursor() as cursor:
                        # SQL
                        sql = "UPDATE passport SET " \
                              "date_of_birth = '%s', surname = '%s', firstname = '%s', " \
                              "patronymic = '%s', address = '%s', building = '%s', phone ='%s'," \
                              "email = '%s',gender = '%d' WHERE id_passport = %d "\
                              % (date_of_birth, surname,firstname,patronymic,address,building,phone,email,gender, id_pass)
                        cursor.execute(sql)
                        connection.commit()
                        self.fields_disable(True)
                        self.prevpatients()
                except Exception:
                    print('problem in update_passto_table function')
        else:
            print('ready to edit')

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ContextMenu:
            menu = QtWidgets.QMenu(self)
            menu.addAction(self.context_menu_1)
            menu.addAction(self.context_menu_2)
            menu.addAction(self.context_menu_3)
            menu.addAction(self.context_menu_4)
            menu.exec_(event.globalPos())
            return True
        return False



    def copy_action(self):
        row = self.tableWidgetPreviousPatients.currentItem().row()
        id = int(self.tableWidgetPreviousPatients.item(row, 0).text())
        self.insert_in_passport(id)

    def new_record(self):
        self.fields_disable(False)
        try:
            self.dateEditDateOfBirth.setDate(QtCore.QDate(1800, 1, 1))
            self.lineEditSurname.setText('')
            self.comboBoxFirstName.setCurrentText('')
            self.comboBoxPatronimicName.setCurrentText('')
            self.comboBoxAdress.setText('')
            self.lineEditHouseRoom.setText('')
            self.lineEditPhone.setText('')
            self.lineEditEmail.setText('')
            self.comboBoxGender.setCurrentIndex(0)
            self.lineEdit_id_passport.setText(str(0))
            self.lineEdit_id_case.setText(str(0))
        except Exception:
            print('problem in new_record function')


    def age(self):
        age = ''
        connection.ping()
        try:
            with connection.cursor() as cursor:
                # SQL
                sql = "SELECT TIMESTAMPDIFF(YEAR, '%s',curdate()) AS age" % (self.dateEditDateOfBirth.date().toPyDate())
                cursor.execute(sql)
                for row in cursor:
                    age = str(row['age'])
                if ((int(age) % 10) == 1):
                    age = age + ' год'
                elif ((int(age) % 10) > 4 or (int(age) % 10) == 0):
                    age = age + ' лет'
                else:
                    age = age + ' года'
                self.lineEditAge.setText(age)


        except Exception:
            print('problem in age function')
        finally:
            pass

    def fields_disable(self, tru):
        self.comboBoxGender.setDisabled(tru)
        self.dateEditDateOfBirth.setDisabled(tru)
        self.lineEditSurname.setDisabled(tru)
        self.comboBoxFirstName.setDisabled(tru)
        self.comboBoxPatronimicName.setDisabled(tru)
        self.comboBoxAdress.setDisabled(tru)
        self.lineEditHouseRoom.setDisabled(tru)
        self.lineEditPhone.setDisabled(tru)
        self.lineEditEmail.setDisabled(tru)

    def editbutton(self, event):
        if(not(self.lineEditSurname.isEnabled())):
            reply = QMessageBox.question(self, 'Attention',
                                         "Are you sure to change this? You may loose current data", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.fields_disable(False)


    def names_input(self):
        #print(self.sender().objectName())
        bcgclr = '#CCFFFF'
        frgndclr = 'green'
        sur = self.lineEditSurname.text()
        nam = self.comboBoxFirstName.currentText()
        patron = self.comboBoxPatronimicName.currentText()
        add = '%'
        if(sur == nam == patron == ''):
            add = ''
            connection.ping()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT id_passport, id_cases, " \
                          "name, date_of_birth, manipulation_short, id_time_begin  " \
                          "FROM previouspatients WHERE surname LIKE '%s' AND firstname LIKE '%s' " \
                          "AND patronymic LIKE '%s' LIMIT 10" % (sur + add, nam + add, patron + add)
                cursor.execute(sql)
                self.treeWidgetPatientMatch.clear()
                id_pass = -1
                for row in cursor:
                    if (id_pass != row['id_passport']):
                        pat = QTreeWidgetItem(['pass' + str(row['id_passport']), row['name'], str(row['date_of_birth'])])
                        self.treeWidgetPatientMatch.addTopLevelItem(pat)
                        if(row['manipulation_short']):
                            pat_child = QTreeWidgetItem\
                                (['case' + str(row['id_cases']),'  Record: ' + row['manipulation_short'], str(row['id_time_begin'])])
                            pat.addChild(pat_child)
                            pat_child.setForeground(1, QtGui.QColor(frgndclr))
                    else:
                        pat_child = QTreeWidgetItem\
                            (['case' + str(row['id_cases']), '  Record: ' + row['manipulation_short'], str(row['id_time_begin'])])
                        pat.addChild(pat_child)
                        # pat_child.setBackground(1, QtGui.QColor(bcgclr))
                        pat_child.setForeground(1, QtGui.QColor(frgndclr))


                    id_pass = row['id_passport']
                    self.treeWidgetPatientMatch.expandToDepth(0)
        except Exception:
            print('problem in namesinput')

    # @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    # def from_tree_to_cases(self, it, col):
     #   print(it, col, it.text(col))

    #@QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def tree_clicked(self, it, col):
        id = it.text(0)[4:]
        if(it.text(0)[0:4] == 'pass'):
            self.insert_in_passport(id)
        elif(it.text(0)[0:4] == 'case'):
            self.lineEdit_id_case.setText(id)
            self.case_select_and_insert_to_comboboxes()


    def insert_in_passport(self, id):
        connection.ping()
        try:
            with connection.cursor() as cursor:
                # SQL
                sql = "SELECT *  FROM passport WHERE id_passport = %d" % (int(id))
                cursor.execute(sql)
                for row in cursor:
                    sex = abs(row['gender'])
                    self.comboBoxGender.setCurrentIndex(sex)
                    self.dateEditDateOfBirth.setDate(QtCore.QDate(row['date_of_birth']))
                    self.lineEditSurname.setText(row['surname'])
                    self.comboBoxFirstName.setCurrentText(row['firstname'])
                    self.comboBoxPatronimicName.setCurrentText(row['patronymic'])
                    self.comboBoxAdress.setText(row['address'])
                    self.lineEditHouseRoom.setText(row['building'])
                    self.lineEditPhone.setText(row['phone'])
                    self.lineEditEmail.setText(row['email'])
                    self.lineEdit_id_passport.setText(str(row['id_passport']))
                    self.lineEdit_id_case.setText('0')
                    self.new_case()
                self.fields_disable(True)
        except Exception:
            print('problem in insert_in_passport function')

    def prevpatients(self):
        index = 0
        connection.ping()
        try:
            with connection.cursor() as cursor:
                # SQL
                sql = "SELECT * FROM previouspatients ORDER BY id_time_begin DESC LIMIT 100"
                cursor.execute(sql)
                for row in cursor:
                    self.tableWidgetPreviousPatients.setItem(index, 0, QTableWidgetItem(str(row['id_passport'])))
                    self.tableWidgetPreviousPatients.setItem(index, 1, QTableWidgetItem(row['name']))
                    self.tableWidgetPreviousPatients.setItem(index, 2, QTableWidgetItem(str(row['date_of_birth'])))
                    self.tableWidgetPreviousPatients.setItem(index, 3, QTableWidgetItem(row['manipulation_short']))
                    self.tableWidgetPreviousPatients.setItem(index, 4, QTableWidgetItem(str(row['id_time_begin'])[:-3]))
                    self.tableWidgetPreviousPatients.setItem(index, 5, QTableWidgetItem(row['doctor']))
                    self.tableWidgetPreviousPatients.setItem(index, 6, QTableWidgetItem(str(row['id_cases'])))
                    index = index + 1

        except Exception:
            print('Это что ещё такое ? def prevpatients(self)')
        finally:
            pass

    # OBSOLETE !!!!!!!!!autofill names and middle names
    @staticmethod
    def namesandpatronyms(sexpick):
        # Подключиться к базе данных.
        connection.ping()
        try:
            gender = True if sexpick else False
            with connection.cursor() as cursor:
                string_list = [[''], ['']]
                # SQL
                sql = "SELECT firstnames FROM firstnames WHERE sex =  %d" % (gender)
                # Выполнить команду запроса (Execute Query).
                cursor.execute(sql)
                # print("cursor.description: ", cursor.description)
                for row in cursor:
                    string_list[0].append(row["firstnames"])

                sql = "SELECT patronymic FROM patronymic WHERE sex =  %d" % (gender)
                # Выполнить команду запроса (Execute Query).
                cursor.execute(sql)
                # print("cursor.description: ", cursor.description)
                for row in cursor:
                    string_list[1].append(row["patronymic"])
        except Exception:
            print('Это что ещё такое? def namesandpatronyms(sexpick)')
        finally:

            # connection.close()

            return string_list

    # Fill the regions
    def connectwbase(self, query):
        # connection = connectutils.getConnection()
        connection.ping()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)

                self.comboBoxRegion.addItem('', '00')
                for result in cursor:
                    tmp = str(result['regions_code'])
                    if len(tmp) < 2:
                        tmp = "0" + tmp
                    self.comboBoxRegion.addItem(result['regions_name_full'], tmp)
                connection.commit()
        except Exception:
            print('problem in connectwbase function')
        finally:
            pass
            # connection.close()

    # streets
    def on_combobox_changed(self):
        value = self.comboBoxRegion.itemData(self.comboBoxRegion.currentIndex())
        if (value == '00' or value == None):
            pass
        else:
            connection.ping()
            try:
                tablename = "addrob" + value
                # establish connection to DB
                query = "SELECT * FROM %s ORDER BY fullname asc" % (tablename)
                # connection = connectutils.getConnection()
                cursor = connection.cursor()
                cursor.execute(query)
                res = [""]
                for result in cursor:
                    res.append(result['fullname'])
                connection.commit()
                # connection.close()
                completer = QCompleter(res, self.comboBoxAdress)
                completer.setCaseSensitivity(False)
                self.comboBoxAdress.setCompleter(completer)
                return res
            except Exception:
                print('problem in on_combobox_changed function')

    def lineeditstreetchanged(self):
        strict = self.comboBoxAdress.text()
        query = "SELECT fullname FROM addrob01 WHERE street LIKE `" + strict + "`"



    # for translation
    def lang_changed(self):
        data = self.comboBoxLang.itemData(self.comboBoxLang.currentIndex())
        if data:
            self.trans.load(data)
            QtWidgets.QApplication.instance().installTranslator(self.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)

    # for translation also
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi(self)
        super(PassportApp, self).changeEvent(event)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    # app.setStyle("fusion")
    window = PassportApp()  # Создаём объект класса PassportApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    connection = connectutils.getConnection()
    main()  # то запускаем функцию main()
