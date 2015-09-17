# -*- coding: utf-8 -*-
'''
    wumappy.gui.common.menubar
    --------------------------

    menu bar management.

    :copyright: Copyright 2014 Lionel Darras and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from PySide import QtCore, QtGui


#---------------------------------------------------------------------------#
# Menu Bar Object                                                           #
#---------------------------------------------------------------------------#
class MenuBar(object):
    '''
    Creates a menu bar object .
    '''
    @classmethod
    def from_list(cls, list, parent):
        '''
        Construct a menu bar object from a list of menubar and functions
        
        Parameters :
        
        :list: list of menu bars and items to build the menubar object.
        
        Returns :
        :menubar: menubar object built with list.

        Example :
        menubar = MenuBar.from_list(List)
        
        '''

        success = True
        mainmenubar = cls()
        mainmenubar.menubarlist = []
        mainmenubar.itemslist = []
        mainmenubar.id = QtGui.QMenuBar(parent.wid)
        mainmenubar.asciiset = parent.asciiset
        mainmenubar.id.setFont(mainmenubar.asciiset.font)
        mainmenubar.list = list

        for item_infos in list:                                     # for each line in the list, representing informations about one item
            id = item_infos[0]                                      # identifiant
            action = item_infos[2]                                  # action type, "Menu", None(=Action)
            parentid = item_infos[4]                                # parent identifiant
            if (parentid == None):                                  # if root menu bar
                found = True
                parentmenubarid = mainmenubar.id                    # parent menu bar identifiant is the root menu bar identifiant
            else:                                                   # if not
                found = False
                menubar = None
                for submenu in mainmenubar.menubarlist:             # for each submenu
                    if (submenu[0] == parentid):                    # if parent identifiant identified
                        found = True
                        parentmenubarid = submenu[1]                
                        break

            if (found == True):                                     # if item can be connected to a menu or submenu
                if (action == "Menu"):                              # sub-menu
                    menubarid = mainmenubar._add_menu(parentmenubarid, item_infos)
                    mainmenubar.menubarlist.append([id,menubarid])  # adds the submenu bar identifiant in the menu bar list
                elif (action == "Separator"):                       # separator
                    mainmenubar._add_separator(parentmenubarid, parent.wid, item_infos)
                elif (action == None):                              # sub-title
                    mainmenubar._add_subtitle(parentmenubarid, parent.wid, item_infos)
                else:                                               # action
                    mainmenubar._add_action(parentmenubarid, parent.wid, item_infos)
                    
        mainmenubar.update()                                        # updates the root menu bar

        return mainmenubar



    def update(self):
                                                                    # sets the new font in all menu and sub menu bar
        for menubar in self.menubarlist:
            menubar[1].setFont(self.asciiset.font)
        self.id.setFont(self.asciiset.font)                         
        self.id.adjustSize()                                        # adjusts the size of menu bar after all font changes
            
        self.width = 0                                              # initialisation of width and height of main menubar
        self.height = 0
        for line in self.itemslist:
            id = line[0]
            isenabled = line[1]
            item_infos = line[2]
            self._enable_item(id, isenabled)                        # enables or disables item

            action = item_infos[2]                  
            if (action == "Menu"):                                  # if action is a sub-menu
                id.setTitle(self.asciiset.getStringValue(item_infos[1]))
            elif (action == "Separator"):                                  # if action is a separator
                id.setSeparator(self.asciiset.getStringValue(item_infos[1]))
            else:                                                   # if action is an action 
                id.setText(self.asciiset.getStringValue(item_infos[1]))

            parentid = item_infos[4]
            
        self.id.adjustSize()                                        # adjusts the size of menu bar after language changes
        self.width = self.id.frameSize().width()
        self.height = self.id.frameSize().height()

                        

    def getmenubarid(self, item_num):
        '''
        Gets the menubarid thanks to an item number defined
        '''
        menubarid = None
        for menubar in self.menubarlist:
            if (item_num == menubar[0]):
                menubarid = menubar[1]
                break
        return menubarid


    def _add_menu(self, menubarid, item):
        '''
        Adds a menu
        '''
        item_name = item[1]
        comment = item[3]
        isenabled = item[5]
        fileMenuid = menubarid.addMenu(item_name)
        self.itemslist.append((fileMenuid, isenabled, item))
        self._enable_item(fileMenuid, isenabled)
        fileMenuid.setToolTip(comment)
        fileMenuid.setFont(self.asciiset.font)
        return fileMenuid


    def _add_action(self, fileMenuid, window, item, checkable=False):
        '''
        Adds an action with an action to do
        '''
        item_name = item[1]
        action = item[2]
        comment = item[3]
        isenabled = item[5]
        actionid = QtGui.QAction(item_name, window)
        actionid.setStatusTip(comment)
        actionid.setToolTip(comment)
        actionid.showStatusText(window)
        actionid.setCheckable(checkable)
        self.itemslist.append((actionid, isenabled, item))
        self._enable_item(actionid, isenabled)
        if (action != None):
            actionid.triggered.connect(action)
        fileMenuid.addAction(actionid)
        fileMenuid.setFont(self.asciiset.font)
        return actionid


    def _add_subtitle(self, fileMenuid, window, item):
        '''
        Adds a sub-title and a separation in the current menu
        '''
        item_name = item[1]
        comment = item[3]
        fileMenuid.addSeparator()
        actionid = QtGui.QAction(item_name, window)
        actionid.setDisabled(True)
        self.itemslist.append((actionid, False, item))
        fileMenuid.setFont(self.asciiset.font)
        fileMenuid.addAction(actionid)
        fileMenuid.addSeparator()
        return actionid
        

    def _add_separator(self, fileMenuid, window, item):
        '''
        Adds a separator in the current menu
        '''
        actionid = None
        fileMenuid.addSeparator()
        return actionid
        

    def _enable_item(self, itemid, isenabled):
        if ((isenabled == True) or (isenabled == False)):
            enabled = isenabled
        else:               # it is a function to execute with a boolean response
            enabled = isenabled()
        itemid.setEnabled(enabled)


    def _check_item(self, itemid, ischecked):
        if ((ischecked == True) or (ischecked == False)):
            checked = ischecked
        else:               # it is a function to execute with a boolean response
            checked = ischecked()
        itemid.setChecked(checked)


