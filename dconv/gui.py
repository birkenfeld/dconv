"""
    dconv.gui
    ~~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""

import sys, os, time
from os import path

from qt import *

from dconv.convdialog_ui import *
from dconv.util import fmt_ex, xdir
from dconv.uitools import *
from dconv.data import OutFormat
from dconv import informats, outformats, convfile, lookup


class ConvDialog(ConvDialogUI):
    def __init__(self, parent=None):
        ConvDialogUI.__init__(self, parent=parent)
        self.infmt.clear()
        self.infmt.insertStrList(xdir(informats))
        self.outfmt.header().hide()
        self.outfmt.clear()
        for fmt in xdir(outformats):
            self.outfmt.insertItem(QListViewItem(self.outfmt, fmt))
        self.outfmt.setSelected(self.outfmt.firstChild(), 1)

        self.indirList = []
        self._warnings = 0
        self._errors = 0
        self.lasttab = None

        dirdefault = "/data/%s" % time.strftime('%Y')

        self.presets = DlgPresets('dconv',
            [(self.input, ''), (self.output, ''),
             (self.multiprefix, ''), (self.multiext, ''),
             (self.multidir, dirdefault), (self.multioutdir, ''),
             (self.infmt, 'mira'), (self.outfmt, ''),
             (self.properties, ''), (self.tabs, 0)])
        self.presets.load()

    def about(self):
        QMessageBox.about(self, "About this tool",
                          "dconv data file conversion tool,\n"
                          "written 2008 by Georg Brandl.")

    def selInput(self):
        selectInputFile(self.input, self)

    def selOutput(self):
        selectOutputFile(self.output, self)

    def selDir(self):
        selectDirectory(self.multidir, self,
                        'Choose an input directory')

    def selOutDir(self):
        selectDirectory(self.multioutdir, self,
                        'Choose an output directory')

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
        viewTextFile(fname, self)

    def refreshClicked(self):
        self.indirChanged()

    def selAll(self):
        self.multifiles.selectAll(True)
    def selNone(self):
        self.multifiles.selectAll(False)

    def outfmtSelected(self, item):
        format = str(item.text(0))
        try:
            format = lookup(format, OutFormat)
        except:
            return
        if format.filename_ext:
            self.multiext.setText(format.filename_ext)

    def outfmtClicked(self, item):
        format = str(item.text(0))
        QMessageBox.information(self, 'Format information', 'This is the '
                                'definition of format %r:\n' % format +
                                getattr(outformats, format))

    def accept(self):
        self.presets.save()
        tab = self.tabs.currentPageIndex()
        if tab > 1:
            if self.lasttab is None:
                QMessageBox.information(self, 'Select conversion mode',
                                        'Please select a "Convert ..." tab.')
                return
            tab = self.lasttab

        infmt = str(self.infmt.currentText())
        outfmt = str(self.outfmt.selectedItem().text(0))
        props = str(self.properties.text()).splitlines()
        aprops = [] # put before the outfmt ones
        bprops = [] # put after the outfmt ones
        for prop in props:
            if prop.strip().startswith('!'):
                aprops.append(prop.strip()[1:])
            else:
                bprops.append(prop)
        outfmt = '\n'.join(aprops) + '\n' + \
                 getattr(outformats, outfmt) + '\n' + \
                 '\n'.join(bprops)

        self.lasttab = tab
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
    runDlgStandalone(ConvDialog)

if __name__ == '__main__':
    main()


