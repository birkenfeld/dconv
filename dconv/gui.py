"""
    dconv.gui
    ~~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""

import sys, os
from os import path
from qt import *

from dconv.ui_convdialog import *
from dconv.util import fmt_ex, xdir
from dconv import informats, outformats, convfile

class DlgPresets(object):
    def __init__(self, group, ctls):
        self.group = group
        self.ctls = ctls

    def load(self):
        settings = QSettings(QSettings.Ini)
        settings.setPath('MIRA', self.group)
        for (ctl, default) in self.ctls:
            entry = 'presets/' + ctl.name()
            if isinstance(default, int):
                val, ok = settings.readNumEntry(entry, default)
            else:
                val, ok = settings.readEntry(entry, default)
            try:
                getattr(self, 'set_' + ctl.__class__.__name__)(ctl, val)
            except:
                pass

    def save(self):
        settings = QSettings(QSettings.Ini)
        settings.setPath('MIRA', self.group)
        for (ctl, _) in self.ctls:
            entry = 'presets/' + ctl.name()
            try:
                val = getattr(self, 'get_' + ctl.__class__.__name__)(ctl)
                settings.writeEntry(entry, val)
            except:
                pass

    def set_QLineEdit(self, ctl, val):
        ctl.setText(val)
    def set_QListBox(self, ctl, val):
        ctl.setSelected(ctl.findItem(val), 1)
    def set_QListView(self, ctl, val):
        ctl.setSelected(ctl.findItem(val, 0), 1)
    def set_QComboBox(self, ctl, val):
        for i in range(ctl.count()):
            if ctl.text(i) == val:
                ctl.setCurrentItem(i)
                return
    def set_QTextEdit(self, ctl, val):
        ctl.setText(val)
    def set_QTabWidget(self, ctl, val):
        ctl.setCurrentPage(val)

    def get_QLineEdit(self, ctl):
        return ctl.text()
    def get_QListBox(self, ctl):
        return ctl.selectedItem().text()
    def get_QListView(self, ctl):
        return ctl.selectedItem().text(0)
    def get_QComboBox(self, ctl):
        return ctl.currentText()
    def get_QTextEdit(self, ctl):
        return ctl.text()
    def get_QTabWidget(self, ctl):
        return ctl.currentPageIndex()


class ConvDialog(ConvDialogGUI):
    def __init__(self, parent=None):
        ConvDialogGUI.__init__(self, parent=parent)
        self.infmt.clear()
        self.infmt.insertStrList(xdir(informats))
        self.outfmt.header().hide()
        self.outfmt.clear()
        for fmt in xdir(outformats):
        #    self.outfmt.insertItem(QCheckListItem(
        #        self.outfmt, fmt, QCheckListItem.CheckBox))
            self.outfmt.insertItem(QListViewItem(self.outfmt, fmt))
        self.outfmt.setSelected(self.outfmt.firstChild(), 1)

        self.indirList = []
        self._warnings = 0
        self._errors = 0

        self.presets = DlgPresets('d2d',
            [(self.input, ''), (self.output, ''),
             (self.multiprefix, ''), (self.multiext, ''),
             (self.multidir, ''), (self.multioutdir, ''),
             (self.infmt, 'mira'), (self.outfmt, ''),
             (self.properties, ''), (self.tabs, 0)])
        self.presets.load()

    def about(self):
        QMessageBox.about(self, "About this tool",
                          "d2d data file conversion tool,\n"
                          "written 2008 by Georg Brandl.")

    def selInput(self):
        previous = str(self.input.text())
        if previous:
            startdir = path.dirname(previous)
        else:
            startdir = '.'
        fname = QFileDialog.getOpenFileName(startdir, 'All files (*)',
                                            self, 'open file dialog',
                                            'Choose an input file')
        if fname:
            self.input.setText(fname)

    def selOutput(self):
        previous = str(self.output.text())
        if previous:
            startdir = path.dirname(previous)
        else:
            startdir = '.'
        fname = QFileDialog.getSaveFileName(startdir, 'All files (*)',
                                            self, 'save file dialog',
                                            'Choose an output filename')
        if fname:
            self.output.setText(fname)

    def selDir(self):
        previous = str(self.multidir.text())
        startdir = previous or '.'
        fname = QFileDialog.getExistingDirectory(
            startdir, self, 'save file dialog',
            'Choose an input directory')
        if fname:
            self.multidir.setText(fname)

    def selOutDir(self):
        previous = str(self.multioutdir.text())
        startdir = previous or '.'
        fname = QFileDialog.getExistingDirectory(
            startdir, self, 'save file dialog',
            'Choose an output directory')
        if fname:
            self.multioutdir.setText(fname)

    def indirChanged(self):
        indir = str(self.multidir.text())
        if not indir or not path.isdir(indir):
            return
        self.indirList = [f for f in os.listdir(indir)
                          if path.isfile(path.join(indir, f))]
        self.indirList.sort()
        self.prefixChanged()

    def prefixChanged(self):
        prefix = str(self.multiprefix.text())
        inlist = [f for f in self.indirList if f.startswith(prefix)]
        self.multifiles.clear()
        self.multifiles.insertStrList(inlist)

    def fileClicked(self, item):
        fname = str(item.text())
        fname = path.join(str(self.multidir.text()), fname)
        if not path.isfile(fname):
            return
        f = open(fname)
        contents = f.read()
        f.close()
        qd = QDialog(self, 'PreviewDlg', True)
        qd.setCaption('File preview')
        qd.resize(QSize(500, 500))
        lay = QVBoxLayout(qd, 11, 6, 'playout')
        lb = QLabel(qd, 'label')
        lb.setText('Viewing %s:' % fname)
        lay.addWidget(lb)
        tx = QTextEdit(qd, 'preview')
        tx.setReadOnly(1)
        tx.setText(contents)
        font = QFont(tx.font())
        font.setFamily('monospace')
        tx.setFont(font)
        lay.addWidget(tx)
        btn = QPushButton(qd, 'ok')
        btn.setAutoDefault(1)
        btn.setDefault(1)
        btn.setText('Close')
        qd.connect(btn, SIGNAL('clicked()'), qd.accept)
        lay.addWidget(btn, 0, QWidget.AlignRight)
        qd.show()

    def refreshClicked(self):
        self.indirChanged()

    def selAll(self):
        self.multifiles.selectAll(True)
    def selNone(self):
        self.multifiles.selectAll(False)

    def outfmtClicked(self, item):
        format = str(item.text(0))
        QMessageBox.information(self, 'Format information', 'This is the '
                                'definition of format %r:\n' % format +
                                getattr(outformats, format))

    def accept(self):
        self.presets.save()
        tab = self.tabs.currentPageIndex()
        if tab > 1:
            QMessageBox.information(self, 'Select conversion mode',
                                    'Please select a "Convert ..." tab.')

        infmt = str(self.infmt.currentText())
        outfmt = str(self.outfmt.selectedItem().text(0))
        props = str(self.properties.text()).splitlines()
        outfmt = getattr(outformats, outfmt)
        outfmt += '\n' + '\n'.join(props)

        if tab == 0:
            self.convertOne(infmt, outfmt)
        elif tab == 1:
            self.convertMulti(infmt, outfmt)

    def warn(self, msg):
        self._warnings += 1
        self.messages.append('<b>Warning:</b> ' + msg.replace('\n', '<br>'))
    def err(self, msg):
        self._errors += 1
        self.messages.append('<b>Error:</b> ' + msg.replace('\n', '<br>'))

    def newConversion(self):
        self._warnings = self._errors = 0
        self.messages.setText('')
        self.tabs.setCurrentPage(2)

    def convertOne(self, infmt, outfmt):
        infile = str(self.input.text())
        outfile = str(self.output.text())
        if not path.exists(infile):
            QMessageBox.warning(self, 'Error', 'Input file doesn\'t exist.')
            return
        if path.exists(outfile):
            if QMessageBox.question(
                self, 'Overwrite file?', 'Output file already exists. '
                'Overwrite it?', QMessageBox.Yes, QMessageBox.No) \
                == QMessageBox.No:
                return

        self.newConversion()

        src = file(infile)
        dest = file(outfile, 'w')
        try:
            convfile(src, dest, infmt, outfmt, self.warn, self.err)
        except Exception, err:
            self.err('Exception while converting %s:\n%s' % (infile, err))
        self.messages.append('<b>Conversion done.</b>')
        src.close()
        dest.close()

    def convertMulti(self, infmt, outfmt):
        indir = str(self.multidir.text())
        outdir = str(self.multioutdir.text())
        suffix = '.' + str(self.multiext.text())
        if suffix == '.':
            QMessageBox.warning(self, 'Error',
                                'New extension shouldn\'t be empty.')
            return
        for dir, name in ((indir, 'Input'), (outdir, 'Output')):
            if not path.isdir(dir):
                QMessageBox.warning(self, 'Error',
                                    '%s directory %r doesn\'t exist.' %
                                    (name, dir))
                return

        srcfiles = []
        for i in range(self.multifiles.count()):
            if self.multifiles.isSelected(i):
                srcfiles.append(
                    path.join(indir, str(self.multifiles.item(i).text())))
        outfiles = [path.join(outdir,
                              path.splitext(path.basename(f))[0] + suffix)
                    for f in srcfiles]
        if not srcfiles:
            QMessageBox.information(self, 'Info',
                                    'No files to convert selected.')
            return

        self.newConversion()

        for infile, outfile in zip(srcfiles, outfiles):
            src = file(infile)
            dest = file(outfile, 'w')
            try:
                convfile(src, dest, infmt, outfmt, self.warn, self.err)
            except Exception, err:
                self.err('Exception while converting %s:\n%s' %
                         (infile, fmt_ex(err)))
            src.close()
            dest.close()
        if self.messages.text().length() == 0:
            self.messages.append(
                'Conversion successful (%d files).' % len(srcfiles))
        else:
            self.messages.append(
                '<b>Conversion done (%d files, %d warnings, %d errors).</b>' %
                (len(srcfiles), self._warnings, self._errors))


def main():
    a = QApplication(sys.argv)
    QObject.connect(a, SIGNAL('lastWindowClosed()'), a, SLOT('quit()'))
    w = ConvDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()

if __name__ == '__main__':
    main()
