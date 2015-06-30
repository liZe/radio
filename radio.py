#!/usr/bin/env python

"""
Radio
=====

:copyright: (c) 2014 by Guillaume Ayoub and contributors.
:license: BSD, see LICENSE for more details.

"""

import configparser
import os
from gi.repository import Gtk, GdkPixbuf, Gst


CONFIG_FOLDER = os.path.expanduser('~/.config/radio')
CONFIG = configparser.SafeConfigParser()
CONFIG.read(os.path.join(CONFIG_FOLDER, 'config'))


class Window(Gtk.ApplicationWindow):
    def __init__(self, application):
        super(Gtk.ApplicationWindow, self).__init__(application=application)
        self.set_title('Radio')
        self.set_icon_name('audio-volume-high')

        self.header = Gtk.HeaderBar()
        self.header.set_title('Radio')
        self.header.set_show_close_button(True)
        self.set_titlebar(self.header)

        self.stop_button = Gtk.Button()
        self.stop_button.add(
            Gtk.Image.new_from_icon_name('media-playback-stop-symbolic', 1))
        self.header.add(self.stop_button)
        self.stop_button.set_sensitive(False)
        self.stop_button.connect('clicked', self.stop)

        self.model = Gtk.ListStore(object)
        self.model.set_column_types((str, str, GdkPixbuf.Pixbuf))

        self.icon_view = Gtk.IconView()
        self.icon_view.set_model(self.model)
        self.icon_view.set_item_width(148)
        self.icon_view.set_text_column(0)
        self.icon_view.set_pixbuf_column(2)
        self.icon_view.set_activate_on_single_click(True)
        self.icon_view.connect('item-activated', self.play)

        scroll = Gtk.ScrolledWindow()
        scroll.add(self.icon_view)
        self.add(scroll)

        Gst.init()
        self.playbin = Gst.ElementFactory.make('playbin', 'player')

        for section in CONFIG.sections():
            icons = [
                filename for filename in os.listdir(CONFIG_FOLDER)
                if filename.startswith(section)]
            if icons:
                icon = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    os.path.join(CONFIG_FOLDER, icons[0]), 128, 128, False)
            else:
                icon = Gtk.IconTheme.get_default().load_icon(
                    'audio-volume-high', 128, Gtk.IconLookupFlags.FORCE_SIZE)
            self.model.append((section, CONFIG[section]['url'], icon))

    def play(self, view, path):
        self.playbin.set_state(Gst.State.NULL)
        self.playbin.set_property('uri', self.model[path][1])
        self.playbin.set_state(Gst.State.PLAYING)
        self.header.set_subtitle(self.model[path][0])
        self.stop_button.set_sensitive(True)

    def stop(self, button):
        self.playbin.set_state(Gst.State.NULL)
        self.header.set_subtitle(None)
        self.stop_button.set_sensitive(False)


class Radio(Gtk.Application):
    def do_activate(self):
        self.window = Window(self)
        self.window.maximize()
        self.window.show_all()


Radio().run()
