#!/usr/bin/env python

"""
Radio
=====

:copyright: (c) 2014 by Guillaume Ayoub and contributors.
:license: BSD, see LICENSE for more details.

"""

import configparser
from pathlib import Path

import gi

gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
gi.require_version('Gst', '1.0')
from gi.repository import Adw, Gst, Gtk  # noqa

CONFIG_FOLDER = Path.home() / '.config' / 'radio'
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_FOLDER / 'config')


class Window(Adw.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title('Radio')
        self.set_icon_name('audio-volume-high')

        header = Adw.HeaderBar()
        self.title = Adw.WindowTitle()
        self.title.set_title('Radio')
        self.title.set_subtitle('')
        header.set_title_widget(self.title)

        self.stop_button = Gtk.Button.new_from_icon_name('media-playback-stop')
        header.pack_start(self.stop_button)
        self.stop_button.set_sensitive(False)
        self.stop_button.connect('clicked', self.stop)

        list_box = Gtk.ListBox()
        for name in CONFIG.sections():
            icons = tuple(CONFIG_FOLDER.glob(f'{name}.*'))
            icon = (
                Gtk.Image.new_from_file(str(icons[0])) if icons else
                Gtk.Image.new_from_icon_name('audio-volume-high'))
            row = Adw.ActionRow(title=name)
            row.add_prefix(icon)
            button = Gtk.Button.new_with_label('▶')
            button.connect('activate', self.play, name, CONFIG[name]['url'])
            row.add_suffix(button)
            row.set_activatable_widget(button)
            list_box.append(row)

        box = Gtk.Box()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(header)
        box.append(list_box)

        self.set_content(box)

        Gst.init([])
        self.playbin = Gst.ElementFactory.make('playbin', 'player')

    def play(self, button, name, uri):
        self.playbin.set_state(Gst.State.NULL)
        self.playbin.set_property('uri', uri)
        self.playbin.set_state(Gst.State.PLAYING)
        self.title.set_subtitle(name)
        self.stop_button.set_sensitive(True)

    def stop(self, button):
        self.playbin.set_state(Gst.State.NULL)
        self.title.set_subtitle('')
        self.stop_button.set_sensitive(False)


class Radio(Adw.Application):
    def do_activate(self):
        self.window = Window(self)
        self.window.maximize()
        self.window.present()


Radio(application_id='fr.yabz.radio').run()
