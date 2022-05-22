#!/usr/bin/env python

"""
Radio
=====

:copyright: (c) 2014 by Guillaume Ayoub and contributors.
:license: BSD, see LICENSE for more details.

"""

import configparser
import os

import gi

gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
gi.require_version('Gst', '1.0')

from gi.repository import Adw, GdkPixbuf, Gst, Gtk  # noqa


CONFIG_FOLDER = os.path.expanduser('~/.config/radio')
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(CONFIG_FOLDER, 'config'))


class Window(Gtk.ApplicationWindow):
    def __init__(self, application):
        super(Gtk.ApplicationWindow, self).__init__(application=application)
        self.set_title('Radio')
        self.set_icon_name('audio-volume-high')

        self.header = Gtk.HeaderBar()
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        box.set_valign(Gtk.Align.CENTER)
        title = Gtk.Label.new('Radio')
        box.append(title)
        self.subtitle = Gtk.Label.new('')
        self.subtitle.hide()
        self.subtitle.set_opacity(0.5)
        box.append(self.subtitle)
        self.header.set_title_widget(box)
        self.set_titlebar(self.header)

        self.stop_button = Gtk.Button.new_from_icon_name('media-playback-stop')
        self.header.pack_start(self.stop_button)
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

        self.set_child(self.icon_view)

        Gst.init([])
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
        self.subtitle.set_text(self.model[path][0])
        self.subtitle.show()
        self.stop_button.set_sensitive(True)

    def stop(self, button):
        self.playbin.set_state(Gst.State.NULL)
        self.subtitle.hide()
        self.stop_button.set_sensitive(False)


class Radio(Adw.Application):
    def __init__(self):
        Adw.Application.__init__(self, application_id='fr.yabz.radio')

    def do_activate(self):
        self.window = Window(self)
        self.window.maximize()
        self.window.show()


Radio().run()
