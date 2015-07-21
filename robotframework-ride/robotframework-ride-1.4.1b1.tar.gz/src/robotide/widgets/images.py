#  Copyright 2008-2015 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import wx
import os


class ImageList(wx.ImageList):

    def __init__(self, img_width, img_height):
        wx.ImageList.__init__(self, img_width, img_height)

    def add(self, image):
        self.Add(image)


class ImageProvider(object):
    _BASE = os.path.dirname(__file__)

    def __init__(self, size=(16, 16)):
        self._size = size
        self.TESTCASEIMG = self._load_image('robot.png')
        self.KEYWORDIMG = self._load_image('process.png')
        self.DATADIRIMG = self._img_from_art_provider(wx.ART_FOLDER)
        self.DATAFILEIMG = self._img_from_art_provider(wx.ART_NORMAL_FILE)
        self.PROGICONS = self._load_prog_icons()
        self.REPORTIMG = self._load_image('report.png')
        self.REFRESH_ALL = self._load_image('database_refresh.png')
        self.KW_SEARCH_ICON = self._load_image('kw_search_button.png')
        self.TEST_SEARCH_ICON = self._load_image('test_search_button.png')
        self.TOOLBAR_PLAY = self._load_image('control_play.png')
        self.TOOLBAR_STOP = self._load_image('control_stop.png')
        self.TOOLBAR_PAUSE = self._load_image('control_pause.png')
        self.TOOLBAR_CONTINUE = self._load_image('control_play.png')
        self.TOOLBAR_NEXT = self._load_image('control_fastforward.png')
        self.SWITCH_FIELDS_ICON = self._load_image('switch.png')
        self._build_icons()

    def _build_icons(self):
        self._icons = {}
        for name in dir(self):
            value = getattr(self, name)
            if isinstance(value, wx.Bitmap):
                self._icons[name] = getattr(self, name)

    def get_image_by_name(self, name):
        return self._icons.get(name, None)

    def _load_image(self, name):
        path = self._get_img_path(name)
        return wx.Image(path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    def _get_img_path(self, name):
        return os.path.join(self._BASE, name)

    def _img_from_art_provider(self, source):
        return wx.ArtProvider_GetBitmap(source, wx.ART_OTHER, self._size)

    def _load_prog_icons(self):
        icons = wx.IconBundle()
        icons.AddIconFromFile(self._get_img_path('robot.ico'),
                             wx.BITMAP_TYPE_ANY)
        return icons
