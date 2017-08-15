#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 0.96(2016-07-20)

@note:
ABOUT EASYKIVY

EasyKivy provides an easy-to-use interface for simple GUI interaction
with a user based on EasyGUI.

@note:
Note that EasyKivy requires Kivy release 1.8.0 or greater.

@note:
LICENSE INFORMATION

EasyKivy version 0.96

Copyright (c) 2016, Juan R. Lama

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer. 
    
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation and/or
       other materials provided with the distribution. 
    
    3. The name of the author may not be used to endorse or promote products derived
       from this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

@note:
ABOUT THE EASYKIVY LICENSE

This license is what is generally known as the "modified BSD license",
aka "revised BSD", "new BSD", "3-clause BSD".
See http://www.opensource.org/licenses/bsd-license.php

This license is GPL-compatible.
See http://en.wikipedia.org/wiki/License_compatibility
See http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses

The BSD License is less restrictive than GPL.
It allows software released under the license to be incorporated into proprietary products. 
Works based on the software may be released under a proprietary license or as closed source software.
http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22.29

"""
egversion = '0.96(2016-07-20)'

__all__ = ['ynbox'
    , 'ccbox'
    , 'boolbox'
    , 'indexbox'
    , 'msgbox'
    , 'buttonbox'
    , 'integerbox'
    , 'multenterbox'
    , 'enterbox'
    , 'exceptionbox'
    , 'choicebox'
    , 'codebox'
    , 'textbox'
    , 'diropenbox'
    , 'fileopenbox'
    , 'filesavebox'
    , 'passwordbox'
    , 'multpasswordbox'
    , 'multchoicebox'
    , 'abouteasykivy'
    , 'egversion'
    , 'egdemo'
    , 'EkStore'
    , 'kLogger'
]

import kivy
kivy.require('1.9.0')

import sys, os, re
import string
import pickle
import traceback
import unicodedata
from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.utils import escape_markup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.rst import RstDocument
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
#from kivy.config import Config
#Config.set('kivy', 'log_level', 'info')

from kivy.core.window import Window
Window.size = (800, 600)
#Window.fullscreen = True

#--------------------------------------------------
# check python version and take appropriate action
#--------------------------------------------------
"""
From the python documentation:

sys.hexversion contains the version number encoded as a single integer. This is
guaranteed to increase with each version, including proper support for non-
production releases. For example, to test that the Python interpreter is at
least version 1.5.2, use:

if sys.hexversion >= 0x010502F0:
    # use some advanced feature
    ...
else:
    # use an alternative implementation or warn the user
    ...
"""


if sys.hexversion >= 0x020600F0:
    runningPython26 = True
else:
    runningPython26 = False

if sys.hexversion >= 0x030000F0:
    runningPython3 = True
else:
    runningPython3 = False

if runningPython3:
    from io import StringIO
else:
    from StringIO import StringIO

rootWindowPosition = "+300+200"

PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY = ("Courier")

PROPORTIONAL_FONT_SIZE = 10
MONOSPACE_FONT_SIZE = 9  #a little smaller, because it it more legible at a smaller size
TEXT_ENTRY_FONT_SIZE = 12  # a little larger makes it easier to see

#STANDARD_SELECTION_EVENTS = ["Return", "Button-1"]
STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]

# Initialize some global variables that will be reset later
__choiceboxMultipleSelect = None
__widgetTexts = None
__replyButtonText = None
__choiceboxResults = None
__firstWidget = None
__enterboxText = None
__enterboxDefaultText = ""
__multenterboxText = ""
choiceboxChoices = None
choiceboxWidget = None
entryWidget = None
boxRoot = None
ImageErrorMsg = (
    "\n\n---------------------------------------------\n"
    "Error: %s\n%s")


def write(*args):
    args = [str(arg) for arg in args]
    args = " ".join(args)
    sys.stdout.write(args)


def writeln(*args):
    write(*args)
    sys.stdout.write("\n")


say = writeln


def dq(s):
    return '"%s"' % s

#--------------------------------------------------
# check python version and take appropriate action
#--------------------------------------------------
"""
From the python documentation:

sys.hexversion contains the version number encoded as a single integer. This is
guaranteed to increase with each version, including proper support for non-
production releases. For example, to test that the Python interpreter is at
least version 1.5.2, use:

if sys.hexversion >= 0x010502F0:
    # use some advanced feature
    ...
else:
    # use an alternative implementation or warn the user
    ...
"""

if sys.hexversion >= 0x020600F0:
    runningPython26 = True
else:
    runningPython26 = False

if sys.hexversion >= 0x030000F0:
    runningPython3 = True
else:
    runningPython3 = False

def uniquify_list_of_strings(input_list):
    """
    Ensure that every string within input_list is unique.
    :param list input_list: List of strings
    :return: New list with unique names as needed.
    """
    output_list = list()
    for i, item in enumerate(input_list):
        tempList = input_list[:i] + input_list[i + 1:]
        if item not in tempList:
            output_list.append(item)
        else:
            output_list.append('{0}_{1}'.format(item, i))
    return output_list

def parse_hotkey(text):
    """
    Extract a desired hotkey from the text.  The format to enclose
    the hotkey in square braces
    as in Button_[1] which would assign the keyboard key 1 to that button.
      The one will be included in the
    button text.  To hide they key, use double square braces as in:  Ex[[qq]]
    it  , which would assign
    the q key to the Exit button. Special keys such as <Enter> may also be
    used:  Move [<left>]  for a full
    list of special keys, see this reference: http://infohoglobal_state.nmt.edu/tcc/help/
    pubs/tkinter/web/key-names.html
    :param text:
    :return: list containing cleaned text, hotkey, and hotkey position within
    cleaned text.
    """

    ret_val = [escape_markup(text), None]  # Default return values
    if text is None:
        return ret_val

    # Single character, remain visible
    res = re.search('(?<=\[).(?=\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = escape_markup(text[:start - 1]) + r'[b]' + text[start:end] + r'[/b]' + escape_markup(text[end + 1:])
        ret_val = [caption, text[start:end]]

    # Single character, hide it
    res = re.search('(?<=\[\[).(?=\]\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 2] + text[end + 2:]
        ret_val = [escape_markup(caption), text[start:end]]

    # a Keysym.  Always hide it
    res = re.search('(?<=\[\<).+(?=\>\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 2] + text[end + 2:]
        ret_val = [escape_markup(caption), '<{}>'.format(text[start:end])]

    return ret_val

class EK_Popup(Popup):
    returnvalue = ObjectProperty(None)
    my_title = StringProperty(u' ')
    my_image = StringProperty(u'')
    my_msg = StringProperty('')
    my_choices = ListProperty(["Button1", "Button2", "Button3"])
    my_guitype = StringProperty(u'buttonbox')
    my_defaulttext = StringProperty(u'')
    my_mask = ObjectProperty(None)
    my_fields = ListProperty([])
    my_values = ListProperty([])
    my_text = StringProperty(u'')
    my_path = StringProperty(u'')
    my_focused_widget = ObjectProperty(None)
    my_ok_widget = ObjectProperty(None)
    my_cancel_widget = ObjectProperty(None)
    send_to = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EK_Popup, self).__init__(**kwargs)
        self._my_guibuild = {
            'buttonbox': self._gui_btnbox,
            'enterbox': self._gui_enterbox,
            'multenterbox': self._gui_multenterbox,
            'choicebox': self._gui_choicebox,
            'multchoicebox': self._gui_multchoicebox,
            'textbox': self._gui_textbox,
            'diropenbox': self._gui_diropenbox,
            'fileopenbox': self._gui_fileopenbox,
            'filesavebox': self._gui_filesavebox,
        }
        self.content = self._my_guibuild[self.my_guitype]()
        if self.my_focused_widget:
            self.my_focused_widget.focused = True


    def _gui_btnbox(self):
        content = BoxLayout(orientation='vertical')
        if self.my_msg != '':
            content.add_widget(Label(text=self.my_msg, valign='middle', size_hint=(1, 1)))
        if self.my_image != '':
            content.add_widget(Image(source=self.my_image))
        if len(self.my_choices) > 0:
            unique_choices = uniquify_list_of_strings(self.my_choices)
            buttons = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
            for row, (button_text, unique_button_text) in enumerate(zip(self.my_choices, unique_choices)):
                this_button = dict()
                this_button['original_text'] = button_text
                this_button['clean_text'], this_button['hotkey'] = parse_hotkey(button_text)
                #this_button['clean_text'] = u"Button [b]1[/b] 1"
                buttons.add_widget(Button(text=this_button['clean_text'], on_release=self.endbtn, markup=True))
            content.add_widget(buttons)
        return content

    def endbtn(self, btn):
        self.returnvalue = btn.text
        self.dismiss()

    def _gui_enterbox(self):
        self.my_choices = ['OK', 'CANCEL']
        content = BoxLayout(orientation='vertical')
        if self.my_msg != '':
            content.add_widget(Label(text=self.my_msg))
        if self.my_image != '':
            content.add_widget(Image(source=self.my_image))
        password = False
        if self.my_mask: password = True
        self.my_focused_widget = TextInput(text=self.my_defaulttext, multiline=False, size_hint=(1, None), height=dp(30), password=password, on_text_validate=self.endtxtok)
        content.add_widget(self.my_focused_widget)
        buttons = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        for choice in self.my_choices:
            buttons.add_widget(Button(text=choice, on_release=self.endtxt))
        content.add_widget(buttons)
        return content

    def endtxtok(self, textinput):
        self.returnvalue = textinput.text
        self.dismiss()

    def endtxt(self, btn):
        if btn.text == 'OK':
            txtwidget = btn.parent.parent
            self.returnvalue = txtwidget.children[1].text
        else:
            self.returnvalue = None
        self.dismiss()

    def _gui_multenterbox(self):
        self.my_choices = ['OK', 'CANCEL']
        content = BoxLayout(orientation='vertical')
        if self.my_msg != '':
            content.add_widget(Label(text=self.my_msg))
        topscroll = ScrollView(do_scroll_x=False)
        fields = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(30) * len(self.my_fields))
        for n, field in enumerate(self.my_fields):
            fieldbox = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
            fieldbox.add_widget(Label(text=field, size_hint_x=.4))
            password = False
            if self.my_mask and (n+1) == len(self.my_fields): password = True
            the_textinput = TextInput(text=self.my_values[n], multiline=False, size_hint_x=.6, password=password, write_tab=False, on_text_validate=self.endmulttxtok)
            if n == 0:
                self.my_focused_widget = the_textinput
            fieldbox.add_widget(the_textinput)
            fields.add_widget(fieldbox)
            
        topscroll.add_widget(fields)
        content.add_widget(topscroll)
        buttons = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        for choice in self.my_choices:
            buttons.add_widget(Button(text=choice, on_release=self.endmulttxt))
        content.add_widget(buttons)
        return content

    def endmulttxtok(self, textinput):
            values = []
            txtwidget = textinput.parent.parent
            for child in txtwidget.children:
                values.append(child.children[0].text)
            self.returnvalue = [i for i in reversed(values)]
            self.dismiss()

    def endmulttxt(self, btn):
        if btn.text == 'OK':
            values = []
            txtwidget = btn.parent.parent.children[1].children[0]
            for child in txtwidget.children:
                values.append(child.children[0].text)
            self.returnvalue = [i for i in reversed(values)]
        else:
            self.returnvalue = None
        self.dismiss()

    def _gui_choicebox(self):
        return self._gui_multchoicebox(multichoice=False)

    def _gui_multchoicebox(self, multichoice=True):
        self.my_choices = ['SELECT ALL', 'CLEAR ALL', 'OK', 'CANCEL']
        content = BoxLayout(orientation='vertical')
        topbar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(60))
        l = Label(text=self.my_msg, halign='left', valign='middle', size_hint=(.7, 1))
        l.bind(size=l.setter('text_size'))
        topbar.add_widget(l)
        if multichoice:
            buttons = BoxLayout(orientation='vertical', size_hint=(None, 1))
            for choice in self.my_choices[:2]:
                buttons.add_widget(Button(text=choice, on_release=self.selectchoice))
            topbar.add_widget(buttons)
        buttons = BoxLayout(orientation='vertical', size_hint=(None, 1))
        for choice in self.my_choices[2:]:
            buttons.add_widget(Button(text=choice, on_release=self.endchoice))
        topbar.add_widget(buttons)
        content.add_widget(topbar)
        bottomscroll = ScrollView(do_scroll_x=False)
        bottomgrid = BoxLayout(orientation='vertical', id='Grid', size_hint=(1, None), height=30 * len(self.my_fields))
        mygroup = bottomgrid.id
        if multichoice:
            mygroup = None
        for row in self.my_fields:
            rowlayout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
            rowlayout.add_widget(CheckBox(group=mygroup, size_hint=(None, 1), width=dp(40)))
            l = Label(text=row, halign='left', valign='middle', size_hint=(None, 1))
            l.bind(texture_size=l.setter('size'))
            rowlayout.add_widget(l)
            bottomgrid.add_widget(rowlayout)
        if mygroup:
            bottomgrid.children[-1].children[1].active = True
        bottomscroll.add_widget(bottomgrid)
        content.add_widget(bottomscroll)
        return content

    def endchoice(self, btn):
        if btn.text == 'OK':
            self.returnvalue = []
            mywindow = btn.get_parent_window()
            mylayout = mywindow.children[0].children[0].children[0].children[0].children[0].children[0]
            for mychildren in mylayout.children:
                if mychildren.children[1].active:
                    self.returnvalue.append(mychildren.children[0].text)
        else:
            self.returnvalue = [None]
        self.dismiss()

    def selectchoice(self, btn):
        setactive = False
        if btn.text == 'SELECT ALL':
            setactive = True
        mywindow = btn.get_parent_window()
        mylayout = mywindow.children[0].children[0].children[0].children[0].children[0].children[0]
        for mychildren in mylayout.children:
            mychildren.children[1].active = setactive

    def _gui_textbox(self):
        content = BoxLayout(orientation='vertical')
        topbar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        l = Label(text=self.my_msg, halign='left', valign='middle', size_hint=(.7, 1))
        l.bind(size=l.setter('text_size'))
        topbar.add_widget(l)
        topbar.add_widget(Button(text='OK', on_release=self.closebtn, size_hint=(None, 1)))
        content.add_widget(topbar)
        content.add_widget(RstDocument(text=self.my_text))
        return content

    def closebtn(self, btn):
        self.returnvalue = ''
        self.dismiss()

    def _gui_diropenbox(self):
        content = BoxLayout(orientation='vertical')
        self.myfilechooser = FileChooserIconView()
        self.myfilechooser.bind(path=self.diropenselect)
        if self.my_text != '': self.myfilechooser.path = self.my_text
        content.add_widget(self.myfilechooser)
        self.mytextinput = TextInput(text=self.myfilechooser.path, readonly=True, halign='left', multiline=False,
                                size_hint=(1, None), height=dp(30))
        content.add_widget(self.mytextinput)
        bottombar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        bottombar.add_widget(Button(text='Cancel', on_release=self.closebtn))
        bottombar.add_widget(Button(text='OK', on_release=self.enddiropen))
        content.add_widget(bottombar)
        return content

    def diropenselect(self, myfilechooser, path):
        if myfilechooser.parent:
            self.mytextinput.text = myfilechooser.path

    def enddiropen(self, btn):
        if btn.text == 'OK':
            self.returnvalue = self.myfilechooser.path
        else:
            self.returnvalue = None
        self.dismiss()

    def _gui_fileopenbox(self):
        mypath = os.path.abspath(self.my_text)
        content = BoxLayout(orientation='vertical')
        toptopbar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        toptopbar.add_widget(Label(text='Folder:', size_hint_x=None))
        mypathlist = mypath.split('/')
        self.myextendedpath = []
        for i, dir in enumerate(mypathlist):
            if i == 0:
                self.myextendedpath.append('/')
            elif i == 1:
                self.myextendedpath.append(self.myextendedpath[-1] + mypathlist[i])
            else:
                self.myextendedpath.append(self.myextendedpath[-1] + '/' + mypathlist[i])
        self.mypathspinner = Spinner(text=self.myextendedpath[-1], values=self.myextendedpath)
        self.mypathspinner.bind(text=self.changedir)
        toptopbar.add_widget(self.mypathspinner)
        toptopbar.add_widget(Button(text='Up', on_release=self.updir, size_hint_x=.2))
        content.add_widget(toptopbar)
        topbar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        topbar.add_widget(Button(text='List', on_release=self.viewfileopen))
        topbar.add_widget(Button(text='Icon', on_release=self.viewfileopen))
        content.add_widget(topbar)
        self.transition = SlideTransition(duration=.35)
        sm = ScreenManager(transition=self.transition)
        screenicon = Screen(name='iconview')
        self.myfilechoosericon = FileChooserIconView(path=mypath)
        self.myfilechoosericon.bind(selection=self.fileopenselect, path=self.fileopenpath)
        screenicon.add_widget(self.myfilechoosericon)
        sm.add_widget(screenicon)
        screenlist = Screen(name='listview')
        self.myfilechooserlist = FileChooserListView(path=mypath)
        self.myfilechooserlist.bind(selection=self.fileopenselect, path=self.fileopenpath)
        screenlist.add_widget(self.myfilechooserlist)
        sm.add_widget(screenlist)
        content.add_widget(sm)
        filename = self.my_mask
        if not filename:
            filename = ''
        self.mytextinput = TextInput(text=filename, readonly=True, halign='left', multiline=False,
                                     size_hint=(1, None),
                                     height=dp(30))
        content.add_widget(self.mytextinput)
        bottombar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        self.myfiltersdict = {}
        default = None
        for filetype in self.my_fields:
            mytext = filetype[0] + ' ('
            for wildcards in filetype[1]:
                mytext += wildcards + ','
            mytext = mytext[:-1] + ')'
            self.myfiltersdict[mytext] = filetype
            if not default:
                default = mytext
        self.myspinner = Spinner(text=default, values=self.myfiltersdict.keys())
        self.myspinner.bind(text=self.selectfiletype)
        setattr(self.myfilechoosericon, 'filters', self.myfiltersdict[default][1])
        setattr(self.myfilechooserlist, 'filters', self.myfiltersdict[default][1])
        bottombar.add_widget(self.myspinner)
        bottombar.add_widget(Button(text='Cancel', on_release=self.closebtn, size_hint_x=.2))
        bottombar.add_widget(Button(text='OK', on_release=self.endfileopen, size_hint_x=.2))
        content.add_widget(bottombar)
        return content

    def updir(self, button):
        if self.mypathspinner.text == self.mypathspinner.text[0]:
            return
        else:
            self.mypathspinner.text = self.mypathspinner.values[-2]

    def changedir(self, spinner, select):
        self.myfilechooserlist.path = select
        self.myfilechoosericon.path = select
        mypathlist = select.split('/')
        self.myextendedpath = []
        for i, dir in enumerate(mypathlist):
            if i == 0:
                self.myextendedpath.append('/')
            elif i == 1:
                self.myextendedpath.append(self.myextendedpath[-1] + mypathlist[i])
            else:
                self.myextendedpath.append(self.myextendedpath[-1] + '/' + mypathlist[i])
        self.mypathspinner.values = self.myextendedpath


    def selectfiletype(self, spinner, select):
        setattr(self.myfilechoosericon, 'filters', self.myfiltersdict[select][1])
        setattr(self.myfilechooserlist, 'filters', self.myfiltersdict[select][1])

    def viewfileopen(self, btn):
        sm = btn.parent.parent.children[2]
        if btn.text == 'List':
            self.transition.direction = 'right'
            sm.current = 'listview'
        else:
            self.transition.direction = 'left'
            sm.current = 'iconview'

    def fileopenselect(self, myfilechooser, selection):
        sm = myfilechooser.parent.parent
        myname = myfilechooser.parent.name
        if not sm:
            return
        #textinputwidget = myfilechooser.parent.parent.parent.children[1]
        mypath = myfilechooser.path
        myselection = myfilechooser.selection
        if selection:
            self.mytextinput.text = os.path.basename(myfilechooser.selection[0])
        else:
            self.mytextinput.text = ''
        if myname == 'iconview':
            self.myfilechooserlist.path = mypath
            self.myfilechooserlist.selection = myselection
        else:
            self.myfilechoosericon.path = mypath
            self.myfilechoosericon.selection = myselection
        self.mypathspinner.text = mypath


    def fileopenpath(self, myfilechooser, path):
        sm = myfilechooser.parent.parent
        myname = myfilechooser.parent.name
        if not sm:
            return
        #textinputwidget = myfilechooser.parent.parent.parent.children[1]
        if myname == 'iconview':
            self.myfilechooserlist.path = path
            self.myfilechooserlist.selection = ''
            #screenicon = sm.get_screen('iconview')
            #screenicon.children[0].path = path
        else:
            self.myfilechoosericon.path = path
            self.myfilechoosericon.selection = ''
            #screenlist = sm.get_screen('listview')
            #screenlist.children[0].path = path
        if path:
            self.mypathspinner.text = os.path.normpath(path)
            self.mytextinput.text = ''
            #textinputwidget.text = path + '/'
            #else:
            #textinputwidget.text = ''

    def endfileopen(self, btn):
        if btn.text == 'OK':
            #filechooserwidget = btn.parent.parent.children[2].children[0].children[0]
            text = self.myfilechoosericon.selection
            if text:
                self.returnvalue = text[0]
            else:
                self.returnvalue = None
        else:
            self.returnvalue = None
        self.dismiss()

    def _gui_filesavebox(self):
        content = self._gui_fileopenbox()
        setattr(self.mytextinput, 'readonly', False)
        return content


class EK_App(App):
    returnvalue = ObjectProperty(None)
    my_title = StringProperty(u' ')
    my_image = StringProperty(u'')
    my_msg = StringProperty('')
    my_choices = ListProperty(["Button1", "Button2", "Button3"])
    my_guitype = StringProperty(u'buttonbox')
    my_defaulttext = StringProperty(u'')
    my_mask = ObjectProperty(None)
    my_fields = ListProperty([])
    my_values = ListProperty([])
    my_text = StringProperty(u'')
    my_path = StringProperty(u'')

    def build(self):
        self._sm = ScreenManager()
        self.title = unicodedata.normalize('NFKD', unicode(self.my_title)).encode('ascii','ignore')
        return self._sm

    def on_start(self):
        self.mypopup = EK_Popup(title=self.my_title, size_hint=(1, 1), auto_dismiss=False
                                , my_title = self.my_title
                                , my_image = self.my_image
                                , my_msg = self.my_msg
                                , my_choices = self.my_choices
                                , my_guitype = self.my_guitype
                                , my_defaulttext = self.my_defaulttext
                                , my_mask = self.my_mask
                                , my_fields = self.my_fields
                                , my_values = self.my_values
                                , my_text = self.my_text
                                , my_path = self.my_path
                                , on_dismiss = self.stop
        )
        self.mypopup.open()


    def on_stop(self):
        self.returnvalue = self.mypopup.returnvalue
        self._sm.clear_widgets()
        self.mypopup.clear_widgets()

#-------------------------------------------------------------------
# various boxes built on top of the basic buttonbox
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# ynbox
#-----------------------------------------------------------------------
def ynbox(msg="Shall I continue?"
          , title=" "
          , choices=("Yes", "No")
          , image=None
          , root = None
):
    """
    Display a msgbox with choices of Yes and No.

    The default is "Yes".

    The returned value is calculated this way::
        if the first choice ("Yes") is chosen, or if the dialog is cancelled:
            return 1
        else:
            return 0

    If invoked without a msg argument, displays a generic request for a confirmation
    that the user wishes to continue.  So it can be used this way::
        if ynbox(): pass # continue
        else: sys.exit(0)  # exit the program

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    return boolbox(msg, title, choices, image=image, root = root)


#-----------------------------------------------------------------------
# ccbox
#-----------------------------------------------------------------------
def ccbox(msg="Shall I continue?"
          , title=" "
          , choices=("Continue", "Cancel")
          , image=None
          , root = None
):
    """
    Display a msgbox with choices of Continue and Cancel.

    The default is "Continue".

    The returned value is calculated this way::
        if the first choice ("Continue") is chosen, or if the dialog is cancelled:
            return 1
        else:
            return 0

    If invoked without a msg argument, displays a generic request for a confirmation
    that the user wishes to continue.  So it can be used this way::

        if ccbox():
            pass # continue
        else:
            sys.exit(0)  # exit the program

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    return boolbox(msg, title, choices, image=image, root = root)


#-----------------------------------------------------------------------
# boolbox
#-----------------------------------------------------------------------
def boolbox(msg="Shall I continue?"
            , title=" "
            , choices=("Yes", "No")
            , image=None
            , root = None
):
    """
    Display a boolean msgbox.

    The default is the first choice.

    The returned value is calculated this way::
        if the first choice is chosen, or if the dialog is cancelled:
            returns 1
        else:
            returns 0
    """
    reply = buttonbox(msg=msg, choices=choices, title=title, image=image, root = root)
    if reply == choices[0]:
        return 1
    else:
        return 0


#-----------------------------------------------------------------------
# indexbox
#-----------------------------------------------------------------------
def indexbox(msg="Shall I continue?"
             , title=" "
             , choices=("Yes", "No")
             , image=None
             , root = None
):
    """
    Display a buttonbox with the specified choices.
    Return the index of the choice selected.
    """
    reply = buttonbox(msg=msg, choices=choices, title=title, image=image, root = root)
    index = -1
    for choice in choices:
        index = index + 1
        if reply == choice: return index
    raise AssertionError(
        "There is a program logic error in the EasyGui code for indexbox.")


#-----------------------------------------------------------------------
# msgbox
#-----------------------------------------------------------------------
def msgbox(msg="(Your message goes here)", title=" ", ok_button="OK", image=None, root=None):
    """
    Display a messagebox
    """
    if type(ok_button) != type("OK"):
        raise AssertionError("The 'ok_button' argument to msgbox must be a string.")

    return buttonbox(msg=msg, title=title, choices=[ok_button], image=image, root=root)


def buttonbox(msg="", title=" "
              , choices=("Button 1", "Button 2", "Button 3")
              , image=None
              , root=None
):
    """
    Display a msg, a title, and a set of buttons.
    The buttons are defined by the members of the choices list.
    Return the text of the button that the user selected.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    if image:
        image_kv = '''
    Image:
        source: "''' + image + '"'
    else:
        image_kv = ''

    if image == None:
        image = ''
    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=title, auto_dismiss=False, on_dismiss = root,
                                my_msg=msg, my_title=title, my_choices=choices, my_image=image)
        theroot.mypopup.open()
    else:
        my_EK = EK_App(my_msg=msg, my_title=title, my_choices=choices, my_image=image)
        my_EK.run()
        return my_EK.returnvalue


#-------------------------------------------------------------------
# integerbox
#-------------------------------------------------------------------
def integerbox(msg=""
               , title=" "
               , default=""
               , lowerbound=0
               , upperbound=99
               , image=None
               , root=None
               , **invalidKeywordArguments
):
    """
    Show a box in which a user can enter an integer.

    In addition to arguments for msg and title, this function accepts
    integer arguments for "default", "lowerbound", and "upperbound".

    The default argument may be None.

    When the user enters some text, the text is checked to verify that it
    can be converted to an integer between the lowerbound and upperbound.

    If it can be, the integer (not the text) is returned.

    If it cannot, then an error msg is displayed, and the integerbox is
    redisplayed.

    If the user cancels the operation, None is returned.

    NOTE that the "argLowerBound" and "argUpperBound" arguments are no longer
    supported.  They have been replaced by "upperbound" and "lowerbound".
    """
    if "argLowerBound" in invalidKeywordArguments:
        raise AssertionError(
            "\nintegerbox no longer supports the 'argLowerBound' argument.\n"
            + "Use 'lowerbound' instead.\n\n")
    if "argUpperBound" in invalidKeywordArguments:
        raise AssertionError(
            "\nintegerbox no longer supports the 'argUpperBound' argument.\n"
            + "Use 'upperbound' instead.\n\n")

    if default != "":
        if type(default) != type(1):
            raise AssertionError(
                "integerbox received a non-integer value for "
                + "default of " + dq(str(default)), "Error")

    if type(lowerbound) != type(1):
        raise AssertionError(
            "integerbox received a non-integer value for "
            + "lowerbound of " + dq(str(lowerbound)), "Error")

    if type(upperbound) != type(1):
        raise AssertionError(
            "integerbox received a non-integer value for "
            + "upperbound of " + dq(str(upperbound)), "Error")

    if msg == "":
        msg = ("Enter an integer between " + str(lowerbound)
               + " and "
               + str(upperbound)
        )

    while 1:
        reply = enterbox(msg, title, str(default), image=image, root=root)
        if reply == None: return None

        try:
            reply = int(reply)
        except:
            msgbox("The value that you entered:\n  %s\nis not an integer." % dq(str(reply))
                   , "Error")
            continue

        if reply < lowerbound:
            msgbox("The value that you entered is less than the lower bound of "
                   + str(lowerbound) + ".", "Error")
            continue

        if reply > upperbound:
            msgbox("The value that you entered is greater than the upper bound of "
                   + str(upperbound) + ".", "Error")
            continue

        # reply has passed all validation checks.
        # It is an integer between the specified bounds.
        return reply


def enterbox(msg="Enter something."
             , title=" "
             , default=""
             , strip=True
             , image=None
             , root=None
):
    """
    Show a box in which a user can enter some text.

    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.

    Returns the text that the user entered, or None if he cancels the operation.

    By default, enterbox strips its result (i.e. removes leading and trailing
    whitespace).  (If you want it not to strip, use keyword argument: strip=False.)
    This makes it easier to test the results of the call::

        reply = enterbox(....)
        if reply:
            ...
        else:
            ...
    """
    result = __fillablebox(msg, title, default=default, mask=None, image=image, root=root)
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter your password."
                , title=" "
                , default=""
                , image=None
                , root=None
):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """
    return __fillablebox(msg, title, default, mask="*", image=image, root=root)


def __fillablebox(msg
                  , title=""
                  , default=""
                  , mask=None
                  , image=None
                  , root=None
):
    """
    Show a box in which a user can enter some text.
    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """
    if image:
        image_kv = '''
    Image:
        source: "''' + image + '"'
    else:
        image_kv = ''

    if image == None:
        image = ''

    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=title, auto_dismiss=False, on_dismiss = root,
                                my_msg=msg, my_title=title, my_defaulttext=default, my_image=image, my_guitype='enterbox',
                                my_mask=mask)
        theroot.mypopup.open()
    else:
        my_EK = EK_App(my_msg=msg, my_title=title, my_defaulttext=default, my_image=image, my_guitype='enterbox',
                       my_mask=mask)
        my_EK.run()
        return my_EK.returnvalue


#-------------------------------------------------------------------
# multenterbox
#-------------------------------------------------------------------
def multenterbox(msg="Fill in values for the fields."
                 , title=" "
                 , fields=()
                 , values=()
                 , root = None
):
    r"""
    Show screen with multiple data entry fields.

    If there are fewer values than names, the list of values is padded with
    empty strings until the number of values is the same as the number of names.

    If there are more values than names, the list of values
    is truncated so that there are as many values as names.

    Returns a list of the values of the fields,
    or None if the user cancels the operation.

    Here is some example code, that shows how values returned from
    multenterbox can be checked for validity before they are accepted::
        ----------------------------------------------------------------------
        msg = "Enter your personal information"
        title = "Credit Card Application"
        fieldNames = ["Name","Street Address","City","State","ZipCode"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "":
                break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        writeln("Reply was: %s" % str(fieldValues))
        ----------------------------------------------------------------------

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg fields: a list of fieldnames.
    @arg values:  a list of field values
    """
    return __multfillablebox(msg, title, fields, values, None, root = root)


#-----------------------------------------------------------------------
# multpasswordbox
#-----------------------------------------------------------------------
def multpasswordbox(msg="Fill in values for the fields."
                    , title=" "
                    , fields=tuple()
                    , values=tuple()
                    , root = None
):
    r"""
    Same interface as multenterbox.  But in multpassword box,
    the last of the fields is assumed to be a password, and
    is masked with asterisks.

    Example
    =======

    Here is some example code, that shows how values returned from
    multpasswordbox can be checked for validity before they are accepted::
        msg = "Enter logon information"
        title = "Demo of multpasswordbox"
        fieldNames = ["Server ID", "User ID", "Password"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multpasswordbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
            fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

        writeln("Reply was: %s" % str(fieldValues))
    """
    return __multfillablebox(msg, title, fields, values, "*", root = root)


#-----------------------------------------------------------------------
# __multfillablebox
#-----------------------------------------------------------------------
def __multfillablebox(msg="Fill in values for the fields."
                      , title=" "
                      , fields=()
                      , values=()
                      , mask=None
                      , root = None
):
    if len(fields) == 0: return None

    fields = list(fields[:])  # convert possible tuples to a list
    values = list(values[:])  # convert possible tuples to a list

    if len(values) == len(fields):
        pass
    elif len(values) > len(fields):
        fields = fields[0:len(values)]
    else:
        while len(values) < len(fields):
            values.append("")


    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=title, auto_dismiss=False, on_dismiss = root,
                                my_fields=fields, my_title=title, my_values=values, my_guitype='multenterbox',
                                my_mask=mask)
        theroot.mypopup.open()
    else:
        my_EK = EK_App(my_fields=fields, my_title=title, my_values=values, my_guitype='multenterbox', my_mask=mask)
        my_EK.run()
        return my_EK.returnvalue


#-------------------------------------------------------------------
# multchoicebox
#-------------------------------------------------------------------
def multchoicebox(msg="Pick as many items as you like."
                  , title=" "
                  , choices=()
                  , root = None
                  , **kwargs
):
    """
    Present the user with a list of choices.
    allow him to select multiple items and return them in a list.
    if the user doesn't choose anything from the list, return the empty list.
    return None if he cancelled selection.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    if len(choices) == 0: choices = ["Program logic error - no choices were specified."]
    #-------------------------------------------------------------------
    # If choices is a tuple, we make it a list so we can sort it.
    # If choices is already a list, we make a new list, so that when
    # we sort the choices, we don't affect the list object that we
    # were given.
    #-------------------------------------------------------------------
    choices = list(choices[:])

    # make sure all choices are strings
    for index in range(len(choices)):
        choices[index] = str(choices[index])
    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=title, auto_dismiss=False, on_dismiss = root,
                                my_msg=msg, my_fields=choices, my_title=title, my_guitype='multchoicebox')
        theroot.mypopup.open()
    else:
        my_EK = EK_App(my_msg=msg, my_fields=choices, my_title=title, my_guitype='multchoicebox')
        my_EK.run()
        return my_EK.returnvalue


#-----------------------------------------------------------------------
# choicebox
#-----------------------------------------------------------------------
def choicebox(msg="Pick something."
              , title=" "
              , choices=()
              , root = None
):
    """
    Present the user with a list of choices.
    return the choice that he selects.
    return None if he cancels the selection selection.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    if len(choices) == 0: choices = ["Program logic error - no choices were specified."]
    #-------------------------------------------------------------------
    # If choices is a tuple, we make it a list so we can sort it.
    # If choices is already a list, we make a new list, so that when
    # we sort the choices, we don't affect the list object that we
    # were given.
    #-------------------------------------------------------------------
    choices = list(choices[:])

    # make sure all choices are strings
    for index in range(len(choices)):
        choices[index] = str(choices[index])
    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=title, auto_dismiss=False, on_dismiss = root,
                                my_msg=msg, my_fields=choices, my_title=title, my_guitype='choicebox')
        theroot.mypopup.open()
    else:
        my_EK = EK_App(my_msg=msg, my_fields=choices, my_title=title, my_guitype='choicebox')
        my_EK.run()
        if my_EK.returnvalue:
            return my_EK.returnvalue[0]
        return


#-----------------------------------------------------------------------
# exception_format
#-----------------------------------------------------------------------
def exception_format():
    """
    Convert exception info into a string suitable for display.
    """
    return "".join(traceback.format_exception(
        sys.exc_info()[0]
        , sys.exc_info()[1]
        , sys.exc_info()[2]
    ))


#-----------------------------------------------------------------------
# exceptionbox
#-----------------------------------------------------------------------
def exceptionbox(msg=None, title=None, root = None):
    """
    Display a box that gives information about
    an exception that has just been raised.

    The caller may optionally pass in a title for the window, or a
    msg to accompany the error information.

    Note that you do not need to (and cannot) pass an exception object
    as an argument.  The latest exception will automatically be used.
    """
    if title == None: title = "Error Report"
    if msg == None:
        msg = "An error (exception) has occurred in the program."

    codebox(msg, title, exception_format(), root = root)


#-------------------------------------------------------------------
# codebox
#-------------------------------------------------------------------

def codebox(msg=""
            , title=" "
            , text=""
            , root = None
):
    """
    Display some text in a monospaced font, with no line wrapping.
    This function is suitable for displaying code and text that is
    formatted using spaces.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.
    """
    return textbox(msg, title, text, codebox=1, root = root)


#-------------------------------------------------------------------
# textbox
#-------------------------------------------------------------------
def textbox(msg=""
            , title=" "
            , text=""
            , codebox=0
            , root = None
):
    """
    Display some text in a proportional font with line wrapping at word breaks.
    This function is suitable for displaying general written text.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.
    """

    if msg == None: msg = ""
    if title == None: title = ""

    if type(text) == list() or type(text) == tuple():
        text = string.join(text, sep="\n")

    if codebox:
        text = ".. code::\n" + text
    else:
        text = string.split(text, sep="\n")
        text = string.join(text, sep="\n\n")

    return rstextbox(msg=msg, title=title, text=text, codebox=codebox, root = None)


def rstextbox(msg=""
              , title=" "
              , text=""
              , codebox=2
              , root = None
):
    """
    Display some restructuredtext.

    """

    if msg == None: msg = ""
    if title == None: title = ""
    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=title, auto_dismiss=False, on_dismiss = root,
                                my_msg=msg, my_text=text, my_title=title, my_guitype='textbox')
        theroot.mypopup.open()
    else:
        my_EK = EK_App(my_msg=msg, my_text=text, my_title=title, my_guitype='textbox')
        my_EK.run()
        return my_EK.returnvalue


#-------------------------------------------------------------------
# diropenbox
#-------------------------------------------------------------------
def diropenbox(msg=None
               , title=None
               , default=None
               , root = None
):
    """
    A dialog to get a directory name.
    Note that the msg argument, if specified, is ignored.

    Returns the name of a directory, or None if user chose to cancel.

    If the "default" argument specifies a directory name, and that
    directory exists, then the dialog box will start with that directory.
    """
    title = getFileDialogTitle(msg, title)
    if default == None: default = ""

    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=title, auto_dismiss=False, on_dismiss = root,
                                my_msg=msg, my_text=default, my_title=title, my_guitype='diropenbox')
        theroot.mypopup.open()
        f = theroot.mypopup.returnvalue
    else:
        my_EK = EK_App(my_msg=msg, my_text=default, my_title=title, my_guitype='diropenbox')
        my_EK.run()
        f = my_EK.returnvalue

    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
# getFileDialogTitle
#-------------------------------------------------------------------
def getFileDialogTitle(msg, title):
    if msg and title: return "%s - %s" % (title, msg)
    if msg and not title: return str(msg)
    if title and not msg: return str(title)
    return None  # no message and no title


#-------------------------------------------------------------------
# class FileTypeObject for use with fileopenbox
#-------------------------------------------------------------------
class FileTypeObject:
    def __init__(self, filemask):
        if len(filemask) == 0:
            raise AssertionError('Filetype argument is empty.')

        self.masks = []

        if type(filemask) == type("abc"):  # a string
            self.initializeFromString(filemask)

        elif type(filemask) == type([]):  # a list
            if len(filemask) < 2:
                raise AssertionError('Invalid filemask.\n'
                                     + 'List contains less than 2 members: "%s"' % filemask)
            else:
                self.name = filemask[-1]
                self.masks = list(filemask[:-1])
        else:
            raise AssertionError('Invalid filemask: "%s"' % filemask)

    def __eq__(self, other):
        if self.name == other.name: return True
        return False

    def add(self, other):
        for mask in other.masks:
            if mask in self.masks:
                pass
            else:
                self.masks.append(mask)

    def toTuple(self):
        return (self.name, tuple(self.masks))

    def isAll(self):
        if self.name == "All files": return True
        return False

    def initializeFromString(self, filemask):
        # remove everything except the extension from the filemask
        self.ext = os.path.splitext(filemask)[1]
        if self.ext == "": self.ext = ".*"
        if self.ext == ".": self.ext = ".*"
        self.name = self.getName()
        self.masks = ["*" + self.ext]

    def getName(self):
        e = self.ext
        if e == ".*": return "All files"
        if e == ".txt": return "Text files"
        if e == ".py": return "Python files"
        if e == ".pyc": return "Python files"
        if e == ".xls": return "Excel files"
        if e.startswith("."):
            return e[1:].upper() + " files"
        return e.upper() + " files"


#-------------------------------------------------------------------
# fileopenbox
#-------------------------------------------------------------------
def fileopenbox(msg=None
                , title=None
                , default="*"
                , filetypes=None
                , root = None
):
    """
    A dialog to get a file name.

    About the "default" argument
    ============================
        The "default" argument specifies a filepath that (normally)
        contains one or more wildcards.
        fileopenbox will display only files that match the default filepath.
        If omitted, defaults to "*" (all files in the current directory).

        WINDOWS EXAMPLE::
            ...default="c:/myjunk/*.py"
        will open in directory c:\myjunk\ and show all Python files.

        WINDOWS EXAMPLE::
            ...default="c:/myjunk/test*.py"
        will open in directory c:\myjunk\ and show all Python files
        whose names begin with "test".


        Note that on Windows, fileopenbox automatically changes the path
        separator to the Windows path separator (backslash).

    About the "filetypes" argument
    ==============================
        If specified, it should contain a list of items,
        where each item is either::
            - a string containing a filemask          # e.g. "*.txt"
            - a list of strings, where all of the strings except the last one
                are filemasks (each beginning with "*.",
                such as "*.txt" for text files, "*.py" for Python files, etc.).
                and the last string contains a filetype description

        EXAMPLE::
            filetypes = ["*.css", ["*.htm", "*.html", "HTML files"]  ]

    NOTE THAT
    =========

        If the filetypes list does not contain ("All files","*"),
        it will be added.

        If the filetypes list does not contain a filemask that includes
        the extension of the "default" argument, it will be added.
        For example, if     default="*abc.py"
        and no filetypes argument was specified, then
        "*.py" will automatically be added to the filetypes argument.

    @rtype: string or None
    @return: the name of a file, or None if user chose to cancel

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg default: filepath with wildcards
    @arg filetypes: filemasks that a user can choose, e.g. "*.txt"
    @arg root: parent kivy widget
    """
    ##    localRoot = Tk()
    ##    localRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fileboxSetup(default, filetypes)

    #------------------------------------------------------------
    # if initialfile contains no wildcards; we don't want an
    # initial file. It won't be used anyway.
    # Also: if initialbase is simply "*", we don't want an
    # initialfile; it is not doing any useful work.
    #------------------------------------------------------------
    if (initialfile.find("*") < 0) and (initialfile.find("?") < 0):
        initialfile = None
    elif initialbase == "*":
        initialfile = None

    ##    f = tk_FileDialog.askopenfilename(parent=localRoot
    ##        , title=getFileDialogTitle(msg,title)
    ##        , initialdir=initialdir
    ##        , initialfile=initialfile
    ##        , filetypes=filetypes
    ##        )

    ##    localRoot.destroy()

    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=getFileDialogTitle(msg, title), auto_dismiss=False,
                           my_mask=initialfile, my_fields=filetypes, my_text=initialdir,
                           my_title=getFileDialogTitle(msg, title), my_guitype='fileopenbox', on_dismiss = root)
        theroot.mypopup.open()
        f = theroot.mypopup.returnvalue
    else:
        my_EK = EK_App(my_mask=initialfile, my_fields=filetypes, my_text=initialdir,
                       my_title=getFileDialogTitle(msg, title), my_guitype='fileopenbox')
        my_EK.run()
        f = my_EK.returnvalue
    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
# filesavebox
#-------------------------------------------------------------------
def filesavebox(msg=None
                , title=None
                , default=""
                , filetypes=None
                , root = None
):
    """
    A file to get the name of a file to save.
    Returns the name of a file, or None if user chose to cancel.

    The "default" argument should contain a filename (i.e. the
    current name of the file to be saved).  It may also be empty,
    or contain a filemask that includes wildcards.

    The "filetypes" argument works like the "filetypes" argument to
    fileopenbox.
    """

    # localRoot = Tk()
    # localRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fileboxSetup(default, filetypes)

    # f = tk_FileDialog.asksaveasfilename(parent=localRoot
    #     , title=getFileDialogTitle(msg,title)
    #     , initialfile=initialfile
    #     , initialdir=initialdir
    #     , filetypes=filetypes
    #     )
    # localRoot.destroy()

    if root:
        theroot = root.__self__
        theroot.mypopup = EK_Popup(size_hint = (0.8,0.8), title=getFileDialogTitle(msg, title), auto_dismiss=False, on_dismiss = root,
                            my_mask=initialfile, my_fields=filetypes, my_text=initialdir,
                            my_title=getFileDialogTitle(msg, title), my_guitype='filesavebox')
        theroot.mypopup.open()
        f = theroot.mypopup.returnvalue
    else:
        my_EK = EK_App(my_mask=initialfile, my_fields=filetypes, my_text=initialdir,
                       my_title=getFileDialogTitle(msg, title), my_guitype='filesavebox')
        my_EK.run()
        f = my_EK.returnvalue

    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
#
# fileboxSetup
#
#-------------------------------------------------------------------
def fileboxSetup(default, filetypes):
    if not default: default = os.path.join(".", "*")
    initialdir, initialfile = os.path.split(default)
    if not initialdir: initialdir = "."
    if not initialfile: initialfile = "*"
    initialbase, initialext = os.path.splitext(initialfile)
    initialFileTypeObject = FileTypeObject(initialfile)

    allFileTypeObject = FileTypeObject("*")
    ALL_filetypes_was_specified = False

    if not filetypes: filetypes = []
    filetypeObjects = []

    for filemask in filetypes:
        fto = FileTypeObject(filemask)

        if fto.isAll():
            ALL_filetypes_was_specified = True  # remember this

        if fto == initialFileTypeObject:
            initialFileTypeObject.add(fto)  # add fto to initialFileTypeObject
        else:
            filetypeObjects.append(fto)

    #------------------------------------------------------------------
    # make sure that the list of filetypes includes the ALL FILES type.
    #------------------------------------------------------------------
    if ALL_filetypes_was_specified:
        pass
    elif allFileTypeObject == initialFileTypeObject:
        pass
    else:
        filetypeObjects.insert(0, allFileTypeObject)
    #------------------------------------------------------------------
    # Make sure that the list includes the initialFileTypeObject
    # in the position in the list that will make it the default.
    # This changed between Python version 2.5 and 2.6
    #------------------------------------------------------------------
    if len(filetypeObjects) == 0:
        filetypeObjects.append(initialFileTypeObject)

    if initialFileTypeObject in (filetypeObjects[0], filetypeObjects[-1]):
        pass
    else:
        if runningPython26:
            filetypeObjects.append(initialFileTypeObject)
        else:
            filetypeObjects.insert(0, initialFileTypeObject)

    filetypes = [fto.toTuple() for fto in filetypeObjects]

    return initialbase, initialfile, initialdir, filetypes


#-----------------------------------------------------------------------
#
#     class EgStore
#
#-----------------------------------------------------------------------
class EgStore:
    r"""
A class to support persistent storage.

You can use EgStore to support the storage and retrieval
of user settings for an EasyGui application.


# Example A
#-----------------------------------------------------------------------
# define a class named Settings as a subclass of EgStore
#-----------------------------------------------------------------------
class Settings(EgStore):
::
    def __init__(self, filename):  # filename is required
        #-------------------------------------------------
        # Specify default/initial values for variables that
        # this particular application wants to remember.
        #-------------------------------------------------
        self.userId = ""
        self.targetServer = ""

        #-------------------------------------------------
        # For subclasses of EgStore, these must be
        # the last two statements in  __init__
        #-------------------------------------------------
        self.filename = filename  # this is required
        self.restore()            # restore values from the storage file if possible



# Example B
#-----------------------------------------------------------------------
# create settings, a persistent Settings object
#-----------------------------------------------------------------------
settingsFile = "myApp_settings.txt"
settings = Settings(settingsFile)

user    = "obama_barak"
server  = "whitehouse1"
settings.userId = user
settings.targetServer = server
settings.store()    # persist the settings

# run code that gets a new value for userId, and persist the settings
user    = "biden_joe"
settings.userId = user
settings.store()


# Example C
#-----------------------------------------------------------------------
# recover the Settings instance, change an attribute, and store it again.
#-----------------------------------------------------------------------
settings = Settings(settingsFile)
settings.userId = "vanrossum_g"
settings.store()

"""
    def __init__(self, filename):  # obtaining filename is required
        self.filename = None
        raise NotImplementedError()

    def restore(self):
        """
        Set the values of whatever attributes are recoverable
        from the pickle file.

        Populate the attributes (the __dict__) of the EgStore object
        from     the attributes (the __dict__) of the pickled object.

        If the pickled object has attributes that have been initialized
        in the EgStore object, then those attributes of the EgStore object
        will be replaced by the values of the corresponding attributes
        in the pickled object.

        If the pickled object is missing some attributes that have
        been initialized in the EgStore object, then those attributes
        of the EgStore object will retain the values that they were
        initialized with.

        If the pickled object has some attributes that were not
        initialized in the EgStore object, then those attributes
        will be ignored.

        IN SUMMARY:

        After the recover() operation, the EgStore object will have all,
        and only, the attributes that it had when it was initialized.

        Where possible, those attributes will have values recovered
        from the pickled object.
        """
        if not os.path.exists(self.filename): return self
        if not os.path.isfile(self.filename): return self

        try:
            f = open(self.filename,"rb")
            unpickledObject = pickle.load(f)
            f.close()

            for key in list(self.__dict__.keys()):
                default = self.__dict__[key]
                self.__dict__[key] = unpickledObject.__dict__.get(key,default)
        except:
            pass

        return self

    def store(self):
        """
        Save the attributes of the EgStore object to a pickle file.
        Note that if the directory for the pickle file does not already exist,
        the store operation will fail.
        """
        f = open(self.filename, "wb")
        pickle.dump(self, f)
        f.close()


    def kill(self):
        """
        Delete my persistent file (i.e. pickle file), if it exists.
        """
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        return

    def __str__(self):
        """
        return my contents as a string in an easy-to-read format.
        """
        # find the length of the longest attribute name
        longest_key_length = 0
        keys = []
        for key in self.__dict__.keys():
            keys.append(key)
            longest_key_length = max(longest_key_length, len(key))

        keys.sort()  # sort the attribute names
        lines = []
        for key in keys:
            value = self.__dict__[key]
            key = key.ljust(longest_key_length)
            lines.append("%s : %s\n" % (key,repr(value))  )
        return "".join(lines)  # return a string showing the attributes



#-----------------------------------------------------------------------
#
# test/demo easygui
#
#-----------------------------------------------------------------------
def egdemo():
    """
    Run the EasyGui demo.
    """
    # clear the console
    writeln("\n" * 100)

    intro_message = ("Pick the kind of box that you wish to demo.\n"
                     + "\n * Python version " + sys.version
    )

    #========================================== END DEMONSTRATION DATA


    while 1:  # do forever
        choices = [
            "msgbox",
            "buttonbox",
            "buttonbox(image) -- a buttonbox that displays an image",
            "choicebox",
            "multchoicebox",
            "textbox",
            "ynbox",
            "ccbox",
            "enterbox",
            "enterbox(image) -- an enterbox that displays an image",
            "exceptionbox",
            "codebox",
            "integerbox",
            "boolbox",
            "indexbox",
            "filesavebox",
            "fileopenbox",
            "passwordbox",
            "multenterbox",
            "multpasswordbox",
            "diropenbox",
            "About EasyKivy",
            "Help"
        ]
        choice = choicebox(msg=intro_message
                           , title="EasyKivy " + egversion
                           , choices=choices)

        if not choice: return

        reply = choice.split()

        if reply[0] == "msgbox":
            reply = msgbox("short msg", "This is a long title")
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "About":
            reply = abouteasygui()

        elif reply[0] == "Help":
            _demo_help()

        elif reply[0] == "buttonbox":
            reply = buttonbox()
            writeln("Reply was: %s" % repr(reply))

            title = "Demo of Buttonbox with many, many buttons!"
            msg = "This buttonbox shows what happens when you specify too many buttons."
            reply = buttonbox(msg=msg, title=title, choices=choices)
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "buttonbox(image)":
            _demo_buttonbox_with_image()

        elif reply[0] == "boolbox":
            reply = boolbox()
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "enterbox":
            image = "python_and_check_logo.gif"
            message = "Enter the name of your best friend." \
                      "\n(Result will be stripped.)"
            reply = enterbox(message, "Love!", "     Suzy Smith     ")
            writeln("Reply was: %s" % repr(reply))

            message = "Enter the name of your best friend." \
                      "\n(Result will NOT be stripped.)"
            reply = enterbox(message, "Love!", "     Suzy Smith     ", strip=False)
            writeln("Reply was: %s" % repr(reply))

            reply = enterbox("Enter the name of your worst enemy:", "Hate!")
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "enterbox(image)":
            my_path = os.path.abspath(os.path.dirname(__file__)) + "/"
            image = "python_and_check_logo.gif"
            message = "What kind of snake is this?"
            reply = enterbox(message, "Quiz", image= my_path + image)
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "exceptionbox":
            try:
                thisWillCauseADivideByZeroException = 1 / 0
            except:
                exceptionbox()

        elif reply[0] == "integerbox":
            reply = integerbox(
                "Enter a number between 3 and 333",
                "Demo: integerbox WITH a default value",
                222, 3, 333)
            writeln("Reply was: %s" % repr(reply))

            reply = integerbox(
                "Enter a number between 0 and 99",
                "Demo: integerbox WITHOUT a default value"
            )
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "diropenbox":
            _demo_diropenbox()
        elif reply[0] == "fileopenbox":
            _demo_fileopenbox()
        elif reply[0] == "filesavebox":
            _demo_filesavebox()

        elif reply[0] == "indexbox":
            title = reply[0]
            msg = "Demo of " + reply[0]
            choices = ["Choice1", "Choice2", "Choice3", "Choice4"]
            reply = indexbox(msg, title, choices)
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "passwordbox":
            reply = passwordbox("Demo of password box WITHOUT default"
                                + "\n\nEnter your secret password", "Member Logon")
            writeln("Reply was: %s" % str(reply))

            reply = passwordbox("Demo of password box WITH default"
                                + "\n\nEnter your secret password", "Member Logon", "alfie")
            writeln("Reply was: %s" % str(reply))

        elif reply[0] == "multenterbox":
            msg = "Enter your personal information"
            title = "Credit Card Application"
            fieldNames = ["Name", "Street Address", "City", "State", "ZipCode"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = multenterbox(msg, title, fieldNames)

            # make sure that none of the fields was left blank
            while 1:
                if fieldValues == None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                    if fieldValues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                if errmsg == "": break  # no problems found
                fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

            writeln("Reply was: %s" % str(fieldValues))

        elif reply[0] == "multpasswordbox":
            msg = "Enter logon information"
            title = "Demo of multpasswordbox"
            fieldNames = ["Server ID", "User ID", "Password"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = multpasswordbox(msg, title, fieldNames)

            # make sure that none of the fields was left blank
            while 1:
                if fieldValues == None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                    if fieldValues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                if errmsg == "": break  # no problems found
                fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

            writeln("Reply was: %s" % str(fieldValues))

        elif reply[0] == "ynbox":
            title = "Demo of ynbox"
            msg = "Were you expecting the Spanish Inquisition?"
            reply = ynbox(msg, title)
            writeln("Reply was: %s" % repr(reply))
            if reply:
                msgbox("NOBODY expects the Spanish Inquisition!", "Wrong!")

        elif reply[0] == "ccbox":
            title = "Demo of ccbox"
            reply = ccbox(msg, title)
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "choicebox":
            title = "Demo of choicebox"
            longchoice = "This is an example of a very long option which you may or may not wish to choose." * 2
            listChoices = ["nnn", "ddd", "eee", "fff", "aaa", longchoice
                , "aaa", "bbb", "ccc", "ggg", "hhh", "iii", "jjj", "kkk", "LLL", "mmm", "nnn", "ooo", "ppp", "qqq",
                           "rrr", "sss", "ttt", "uuu", "vvv"]

            msg = "Pick something. " + ("A wrapable sentence of text ?! " * 30) + "\nA separate line of text." * 6
            reply = choicebox(msg=msg, choices=listChoices)
            writeln("Reply was: %s" % repr(reply))

            msg = "Pick something. "
            reply = choicebox(msg=msg, title=title, choices=listChoices)
            writeln("Reply was: %s" % repr(reply))

            msg = "Pick something. "
            reply = choicebox(msg="The list of choices is empty!", choices=[])
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "multchoicebox":
            listChoices = ["aaa", "bbb", "ccc", "ggg", "hhh", "iii", "jjj", "kkk"
                , "LLL", "mmm", "nnn", "ooo", "ppp", "qqq"
                , "rrr", "sss", "ttt", "uuu", "vvv"]

            msg = "Pick as many choices as you wish."
            reply = multchoicebox(msg, "Demo of multchoicebox", listChoices)
            writeln("Reply was: %s" % repr(reply))

        elif reply[0] == "textbox":
            _demo_textbox(reply[0])
        elif reply[0] == "codebox":
            _demo_codebox(reply[0])

        else:
            msgbox("Choice\n\n" + choice + "\n\nis not recognized", "Program Logic Error")
            return


def _demo_textbox(reply):
    text_snippet = (( \
                        """It was the best of times, and it was the worst of times.  The rich ate cake, and the poor had cake recommended to them, but wished only for enough cash to buy bread.  The time was ripe for revolution! """ \
                        * 5) + "\n\n") * 10
    title = "Demo of textbox"
    msg = "Here is some sample text. " * 16
    reply = textbox(msg, title, text_snippet)
    writeln("Reply was: %s" % str(reply))


def _demo_codebox(reply):
    code_snippet = ("dafsdfa dasflkj pp[oadsij asdfp;ij asdfpjkop asdfpok asdfpok asdfpok" * 3) + "\n" + \
                   """# here is some dummy Python code
                   for someItem in myListOfStuff:
                       do something(someItem)
                       do something()
                       do something()
                       if somethingElse(someItem):
                           doSomethingEvenMoreInteresting()

                   """ * 16
    msg = "Here is some sample code. " * 16
    reply = codebox(msg, "Code Sample", code_snippet)
    writeln("Reply was: %s" % repr(reply))


def _demo_buttonbox_with_image():
    msg = "Do you like this picture?\nIt is "
    choices = ["Yes", "No", "No opinion"]
    my_path = os.path.abspath(os.path.dirname(__file__)) + "/"

    for image in [
        "python_and_check_logo.gif"
        , "python_and_check_logo.jpg"
        , "python_and_check_logo.png"
        , "zzzzz.gif"]:
        reply = buttonbox(msg + image, image = my_path + image, choices=choices)
        writeln("Reply was: %s" % repr(reply))


def _demo_help():
    savedStdout = sys.stdout  # save the sys.stdout file object
    sys.stdout = capturedOutput = StringIO()
    help("easygui")
    sys.stdout = savedStdout  # restore the sys.stdout file object
    codebox("EasyGui Help", text=capturedOutput.getvalue())


def _demo_filesavebox():
    filename = "myNewFile.txt"
    title = "File SaveAs"
    msg = "Save file as:"

    f = filesavebox(msg, title, default=filename)
    writeln("You chose to save file: %s" % f)


def _demo_diropenbox():
    title = "Demo of diropenbox"
    msg = "Pick the directory that you wish to open."
    d = diropenbox(msg, title)
    writeln("You chose directory...: %s" % d)

    d = diropenbox(msg, title, default="./")
    writeln("You chose directory...: %s" % d)

    d = diropenbox(msg, title, default="c:/")
    writeln("You chose directory...: %s" % d)


def _demo_fileopenbox():
    msg = "Python files"
    title = "Open files"
    default = "*.py"
    f = fileopenbox(msg, title, default=default)
    writeln("You chose to open file: %s" % f)

    default = "./*.gif"
    filetypes = ["*.jpg", ["*.zip", "*.tgs", "*.gz", "Archive files"], ["*.htm", "*.html", "HTML files"]]
    f = fileopenbox(msg, title, default=default, filetypes=filetypes)
    writeln("You chose to open file: %s" % f)

    """#deadcode -- testing ----------------------------------------
    f = fileopenbox(None,None,default=default)
    writeln("You chose to open file: %s" % f)

    f = fileopenbox(None,title,default=default)
    writeln("You chose to open file: %s" % f)

    f = fileopenbox(msg,None,default=default)
    writeln("You chose to open file: %s" % f)

    f = fileopenbox(default=default)
    writeln("You chose to open file: %s" % f)

    f = fileopenbox(default=None)
    writeln("You chose to open file: %s" % f)
    #----------------------------------------------------deadcode """


def _dummy():
    pass


EASYGUI_ABOUT_INFORMATION = '''
========================================================================
0.96k(2016-07-20)
========================================================================
First version with a new implementation of the EasyGUI Tkinter based 0.96(2010-08-29) to a multiplatform Kivy (+1.8) based.


'''


def abouteasygui():
    """
    shows the easygui revision history
    """
    codebox("About EasyKivy\n" + egversion, "EasyKivy", EASYGUI_ABOUT_INFORMATION)
    return None

def kLogger(msg, info=False):
    """
    Export the Kivy Logger
    """
    if info:
        Logger.info(msg)
    else:     
        Logger.debug(msg)

def main():
    if True:
        egdemo()
    else:
        # test the new feature
        ##        reply = buttonbox("Test buttonbox with kivy", "TEST", choices = ("Hello","World"), image = 'logo.png')
        ##        print "buttonbox: ", reply
        ##        reply = ynbox()
        ##        print "ynbox: ", reply
        ##        reply = ccbox()
        ##        print "ccbox: ", reply
        msgbox("Aplicación de demostración", "Prueba")
        ##        reply = multenterbox("Introduzca un texto ", "Prueba", "textolargo")
        ##        print "enterbox: ", reply
        ##        reply = integerbox("Introduzca un número", "Prueba")
        ##        print "integerbox: ", reply
        ##        msg = "Enter your personal information"
        ##        title = "Credit Card Application"
        ##        fieldNames = ["Name","Street Address","City","State","ZipCode"]
        ##        fieldValues = []  # we start with blanks for the values
        ##        fieldValues = multenterbox(msg,title, fieldNames)
        ##        print "multenterbox: ", fieldValues
        ##        msg = "Select what do you prefer about address and other choices:"
        ##        title = 'Testing'
        ##        choices = ["Name","Street Address","City","State","ZipCode","Other info 1:","Other info 2:","Other info 3:"]
        ##        values = multchoicebox(msg,title, choices)
        ##        print "choicebox: ", values
        ##        msg = "Select what do you prefer:"
        ##        title = 'Testing'
        ##        txt = """
        ##        Textbox test:
        ##        1. Start.
        ##        2. Preparation.
        ##        3. Proccess.
        ##        4. Verify.
        ##        5. End.
        ##        """
        ##        value = textbox(msg, title, txt)
        ##        print "textbox: ", value
        ##        msg = "Select what do you prefer about address and other choices:"
        ##        title = 'Testing'
        ##        value = diropenbox(msg, title, default=None)
        ##        print "diropenbox: ", value
        msg = "Select what do you prefer about address and other choices:"
        title = 'Testing'
        default = "*"
        filetypes = ["*.css", ["*.py", "*.pyc", "Python files"], ["*.htm", "*.html", "HTML files"]]
        value = filesavebox(msg, title, default, filetypes)
        Logger.info("filesavebox: " + str(value))

if __name__ == '__main__':
    main()
