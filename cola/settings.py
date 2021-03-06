# Copyright (c) 2008 David Aguilar
"""This handles saving complex settings such as bookmarks, etc.
"""

import os

from cola import core
from cola import serializer
from cola.models import observable


class SettingsModel(observable.ObservableModel):
    def __init__(self):
        """Load existing settings if they exist"""
        observable.ObservableModel.__init__(self)
        self.bookmarks = []
        self.gui_state = {}

    def add_bookmark(self, bookmark):
        """Adds a bookmark to the saved settings"""
        if bookmark not in self.bookmarks:
            self.bookmarks.append(bookmark)

    def remove_bookmark(self, bookmark):
        """Removes a bookmark from the saved settings"""
        if bookmark in self.bookmarks:
            self.bookmarks.remove(bookmark)


class SettingsManager(object):
    """Manages a SettingsModel singleton
    """
    _settings = None

    # Here we store settings
    _rcfile = os.path.join(core.decode(os.path.expanduser('~')), '.cola')

    @staticmethod
    def settings():
        """Returns the SettingsModel singleton"""
        if not SettingsManager._settings:
            if os.path.exists(SettingsManager._rcfile):
                try:
                    SettingsManager._settings = serializer.load(SettingsManager._rcfile)
                except: # bad json
                    SettingsManager._settings = SettingsModel()
            else:
                SettingsManager._settings = SettingsModel()
        return SettingsManager._settings

    @staticmethod
    def save_gui_state(gui):
        """Saves settings for a cola view"""
        name = gui.name()
        state = gui.export_state()
        model = SettingsManager.settings()
        model.gui_state[name] = state
        SettingsManager.save()

    @staticmethod
    def gui_state(gui):
        """Returns the state for a gui"""
        return SettingsManager.settings().gui_state.get(gui.name(), {})

    @staticmethod
    def save():
        model = SettingsManager.settings()
        serializer.save(model, SettingsManager._rcfile)
