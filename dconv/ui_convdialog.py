# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'convdialog.ui'
#
# Created: Mon Feb 18 13:18:53 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class ConvDialogGUI(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ConvDialog")

        self.setSizeGripEnabled(0)

        ConvDialogLayout = QVBoxLayout(self,11,5,"ConvDialogLayout")

        self.tabs = QTabWidget(self,"tabs")

        self.tab = QWidget(self.tabs,"tab")
        tabLayout = QVBoxLayout(self.tab,11,6,"tabLayout")

        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.textLabel1_3 = QLabel(self.tab,"textLabel1_3")
        layout7.addWidget(self.textLabel1_3)

        self.input = QLineEdit(self.tab,"input")
        layout7.addWidget(self.input)

        self.selectInput = QPushButton(self.tab,"selectInput")
        layout7.addWidget(self.selectInput)
        tabLayout.addLayout(layout7)

        layout6 = QHBoxLayout(None,0,6,"layout6")

        self.textLabel2_2 = QLabel(self.tab,"textLabel2_2")
        layout6.addWidget(self.textLabel2_2)

        self.output = QLineEdit(self.tab,"output")
        layout6.addWidget(self.output)

        self.selectOutput = QPushButton(self.tab,"selectOutput")
        layout6.addWidget(self.selectOutput)
        tabLayout.addLayout(layout6)
        spacer3 = QSpacerItem(26,146,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer3)
        self.tabs.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabs,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        layout7_2 = QHBoxLayout(None,0,6,"layout7_2")

        self.textLabel1_3_2 = QLabel(self.tab_2,"textLabel1_3_2")
        layout7_2.addWidget(self.textLabel1_3_2)

        self.multidir = QLineEdit(self.tab_2,"multidir")
        layout7_2.addWidget(self.multidir)

        self.selectDir = QPushButton(self.tab_2,"selectDir")
        layout7_2.addWidget(self.selectDir)

        tabLayout_2.addMultiCellLayout(layout7_2,0,0,0,1)

        layout7_2_2 = QHBoxLayout(None,0,6,"layout7_2_2")

        self.textLabel_x = QLabel(self.tab_2,"textLabel_x")
        layout7_2_2.addWidget(self.textLabel_x)

        self.multioutdir = QLineEdit(self.tab_2,"multioutdir")
        layout7_2_2.addWidget(self.multioutdir)

        self.selectOutDir = QPushButton(self.tab_2,"selectOutDir")
        layout7_2_2.addWidget(self.selectOutDir)

        tabLayout_2.addMultiCellLayout(layout7_2_2,1,1,0,1)

        layout21 = QVBoxLayout(None,0,6,"layout21")

        self.textLabel3 = QLabel(self.tab_2,"textLabel3")
        self.textLabel3.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel3.sizePolicy().hasHeightForWidth()))
        layout21.addWidget(self.textLabel3)

        self.multiprefix = QLineEdit(self.tab_2,"multiprefix")
        self.multiprefix.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.multiprefix.sizePolicy().hasHeightForWidth()))
        layout21.addWidget(self.multiprefix)

        self.textLabel3_2 = QLabel(self.tab_2,"textLabel3_2")
        self.textLabel3_2.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel3_2.sizePolicy().hasHeightForWidth()))
        layout21.addWidget(self.textLabel3_2)

        self.multiext = QLineEdit(self.tab_2,"multiext")
        self.multiext.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.multiext.sizePolicy().hasHeightForWidth()))
        layout21.addWidget(self.multiext)
        spacer7 = QSpacerItem(21,36,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout21.addItem(spacer7)

        self.selectAll = QPushButton(self.tab_2,"selectAll")
        layout21.addWidget(self.selectAll)

        self.selectNone = QPushButton(self.tab_2,"selectNone")
        layout21.addWidget(self.selectNone)

        tabLayout_2.addLayout(layout21,2,0)

        layout10 = QGridLayout(None,1,1,0,6,"layout10")

        self.refresh = QPushButton(self.tab_2,"refresh")
        self.refresh.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.refresh.sizePolicy().hasHeightForWidth()))

        layout10.addWidget(self.refresh,0,1)

        self.textLabel2_3 = QLabel(self.tab_2,"textLabel2_3")

        layout10.addWidget(self.textLabel2_3,0,0)

        self.multifiles = QListBox(self.tab_2,"multifiles")
        self.multifiles.setSelectionMode(QListBox.Multi)

        layout10.addMultiCellWidget(self.multifiles,1,1,0,1)

        tabLayout_2.addLayout(layout10,2,1)
        self.tabs.insertTab(self.tab_2,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabs,"TabPage")
        TabPageLayout = QVBoxLayout(self.TabPage,11,6,"TabPageLayout")

        self.textLabel1_2 = QLabel(self.TabPage,"textLabel1_2")
        self.textLabel1_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum,0,0,self.textLabel1_2.sizePolicy().hasHeightForWidth()))
        TabPageLayout.addWidget(self.textLabel1_2)

        self.messages = QTextEdit(self.TabPage,"messages")
        self.messages.setEnabled(1)
        self.messages.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.messages.sizePolicy().hasHeightForWidth()))
        self.messages.setTextFormat(QTextEdit.RichText)
        self.messages.setReadOnly(1)
        TabPageLayout.addWidget(self.messages)
        self.tabs.insertTab(self.TabPage,QString.fromLatin1(""))
        ConvDialogLayout.addWidget(self.tabs)

        layout9 = QHBoxLayout(None,0,6,"layout9")

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum,0,0,self.textLabel4.sizePolicy().hasHeightForWidth()))
        layout9.addWidget(self.textLabel4)

        self.infmt = QComboBox(0,self,"infmt")
        layout9.addWidget(self.infmt)
        ConvDialogLayout.addLayout(layout9)

        layout10_2 = QGridLayout(None,1,1,0,6,"layout10_2")

        self.textLabel4_2 = QLabel(self,"textLabel4_2")
        self.textLabel4_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum,0,0,self.textLabel4_2.sizePolicy().hasHeightForWidth()))

        layout10_2.addWidget(self.textLabel4_2,0,0)

        self.properties = QTextEdit(self,"properties")
        self.properties.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred,0,0,self.properties.sizePolicy().hasHeightForWidth()))

        layout10_2.addWidget(self.properties,1,1)

        self.textLabel4_2_2 = QLabel(self,"textLabel4_2_2")

        layout10_2.addWidget(self.textLabel4_2_2,0,1)

        self.outfmt = QListView(self,"outfmt")
        self.outfmt.addColumn(self.__tr("Column 1"))
        self.outfmt.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred,0,0,self.outfmt.sizePolicy().hasHeightForWidth()))
        self.outfmt.setMinimumSize(QSize(0,0))
        self.outfmt.setAllColumnsShowFocus(1)
        self.outfmt.setResizeMode(QListView.AllColumns)

        layout10_2.addWidget(self.outfmt,1,0)
        ConvDialogLayout.addLayout(layout10_2)
        spacer4 = QSpacerItem(20,2,QSizePolicy.Minimum,QSizePolicy.Fixed)
        ConvDialogLayout.addItem(spacer4)

        layout11 = QHBoxLayout(None,0,6,"layout11")

        self.aboutBtn = QPushButton(self,"aboutBtn")
        layout11.addWidget(self.aboutBtn)
        Horizontal_Spacing2 = QSpacerItem(290,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(Horizontal_Spacing2)

        self.ok = QPushButton(self,"ok")
        self.ok.setAutoDefault(1)
        self.ok.setDefault(1)
        layout11.addWidget(self.ok)

        self.cancel = QPushButton(self,"cancel")
        self.cancel.setAutoDefault(1)
        layout11.addWidget(self.cancel)
        ConvDialogLayout.addLayout(layout11)

        self.languageChange()

        self.resize(QSize(538,662).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.ok,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancel,SIGNAL("clicked()"),self.reject)
        self.connect(self.selectDir,SIGNAL("clicked()"),self.selDir)
        self.connect(self.multiprefix,SIGNAL("textChanged(const QString&)"),self.prefixChanged)
        self.connect(self.selectOutDir,SIGNAL("clicked()"),self.selOutDir)
        self.connect(self.selectInput,SIGNAL("clicked()"),self.selInput)
        self.connect(self.selectOutput,SIGNAL("clicked()"),self.selOutput)
        self.connect(self.multidir,SIGNAL("textChanged(const QString&)"),self.indirChanged)
        self.connect(self.selectAll,SIGNAL("clicked()"),self.selAll)
        self.connect(self.selectNone,SIGNAL("clicked()"),self.selNone)
        self.connect(self.outfmt,SIGNAL("doubleClicked(QListViewItem*)"),self.outfmtClicked)
        self.connect(self.aboutBtn,SIGNAL("clicked()"),self.about)
        self.connect(self.multifiles,SIGNAL("doubleClicked(QListBoxItem*)"),self.fileClicked)
        self.connect(self.refresh,SIGNAL("clicked()"),self.refreshClicked)

        self.setTabOrder(self.tabs,self.input)
        self.setTabOrder(self.input,self.selectInput)
        self.setTabOrder(self.selectInput,self.output)
        self.setTabOrder(self.output,self.selectOutput)
        self.setTabOrder(self.selectOutput,self.multidir)
        self.setTabOrder(self.multidir,self.selectDir)
        self.setTabOrder(self.selectDir,self.multioutdir)
        self.setTabOrder(self.multioutdir,self.selectOutDir)
        self.setTabOrder(self.selectOutDir,self.multiprefix)
        self.setTabOrder(self.multiprefix,self.multiext)
        self.setTabOrder(self.multiext,self.multifiles)
        self.setTabOrder(self.multifiles,self.selectAll)
        self.setTabOrder(self.selectAll,self.selectNone)
        self.setTabOrder(self.selectNone,self.messages)
        self.setTabOrder(self.messages,self.ok)
        self.setTabOrder(self.ok,self.cancel)


    def languageChange(self):
        self.setCaption(self.__tr("Data file conversion"))
        self.textLabel1_3.setText(self.__tr("File to convert:"))
        self.selectInput.setText(self.__tr("..."))
        self.textLabel2_2.setText(self.__tr("Target file name:"))
        self.selectOutput.setText(self.__tr("..."))
        self.tabs.changeTab(self.tab,self.__tr("Convert one file"))
        self.textLabel1_3_2.setText(self.__tr("Input directory:"))
        self.selectDir.setText(self.__tr("..."))
        self.textLabel_x.setText(self.__tr("Output directory:"))
        self.selectOutDir.setText(self.__tr("..."))
        self.textLabel3.setText(self.__tr("Prefix filter:"))
        self.textLabel3_2.setText(self.__tr("New extension:"))
        self.selectAll.setText(self.__tr("Select all"))
        self.selectNone.setText(self.__tr("Select none"))
        self.refresh.setText(self.__tr("Refresh"))
        self.textLabel2_3.setText(self.__tr("Files (double-click to preview):"))
        self.multifiles.clear()
        self.multifiles.insertItem(self.__tr("New Item"))
        self.tabs.changeTab(self.tab_2,self.__tr("Convert multiple files"))
        self.textLabel1_2.setText(self.__tr("Conversion messages:"))
        self.tabs.changeTab(self.TabPage,self.__tr("Conversion status"))
        self.textLabel4.setText(self.__tr("Input format:"))
        self.textLabel4_2.setText(self.__tr("Output format (double-click to show):"))
        self.textLabel4_2_2.setText(self.__tr("Additional properties, one per line:"))
        self.outfmt.header().setLabel(0,self.__tr("Column 1"))
        self.outfmt.clear()
        item = QListViewItem(self.outfmt,None)
        item.setText(0,self.__tr("New Item"))

        self.aboutBtn.setText(self.__tr("About"))
        self.ok.setText(self.__tr("Convert"))
        self.ok.setAccel(QString.null)
        self.cancel.setText(self.__tr("Close"))
        self.cancel.setAccel(QString.null)


    def selInput(self):
        print "ConvDialogGUI.selInput(): Not implemented yet"

    def selOutput(self):
        print "ConvDialogGUI.selOutput(): Not implemented yet"

    def selDir(self):
        print "ConvDialogGUI.selDir(): Not implemented yet"

    def prefixChanged(self):
        print "ConvDialogGUI.prefixChanged(): Not implemented yet"

    def selOutDir(self):
        print "ConvDialogGUI.selOutDir(): Not implemented yet"

    def indirChanged(self):
        print "ConvDialogGUI.indirChanged(): Not implemented yet"

    def selAll(self):
        print "ConvDialogGUI.selAll(): Not implemented yet"

    def selNone(self):
        print "ConvDialogGUI.selNone(): Not implemented yet"

    def outfmtClicked(self,a0):
        print "ConvDialogGUI.outfmtClicked(QListViewItem*): Not implemented yet"

    def about(self):
        print "ConvDialogGUI.about(): Not implemented yet"

    def fileClicked(self,a0):
        print "ConvDialogGUI.fileClicked(QListBoxItem*): Not implemented yet"

    def refreshClicked(self):
        print "ConvDialogGUI.refreshClicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ConvDialogGUI",s,c)
