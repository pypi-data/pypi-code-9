
# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
show a table with dotProducts for each reviewer against each proposal *and* assignments
'''


import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtGui
else:
    from PyQt4 import QtGui

import plainTextEdit
import pyRestTable


class Report(plainTextEdit.TextWindow):
    '''
    '''
    
    def __init__(self, parent, agup, settings):
        self.settings = settings
        self.agup = agup
        self.title = 'Analysis Grid'
        text = self.makeText()

        plainTextEdit.TextWindow.__init__(self, parent, self.title, text, self.settings)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.show()
    
    def makeText(self):
        '''
        generate the text of the panel
        '''
        tbl = pyRestTable.Table()
        tbl.labels = ['GUP ID', ] + [rvwr.getFullName() for rvwr in self.agup.reviewers]
        for prop in self.agup.proposals:
            prop_id = prop.getKey('proposal_id')
            row = [prop_id, ]
            assigned = prop.getAssignedReviewers()
            for rvwr in self.agup.reviewers:
                full_name = rvwr.getFullName()
                score = int(100.0*prop.topics.dotProduct(rvwr.topics) + 0.5)
                if full_name in assigned:
                    role = assigned.index(full_name)
                    if role == 0:
                        text = '1: ' + str(score)
                    elif role == 1:
                        text = '2: ' + str(score)
                else:
                    text = score
                row.append(text)
            tbl.rows.append(row)
        return tbl.reST()
    
    def update(self):
        '''
        '''
        text = self.makeText()
        self.setText(text)
        self.show()
