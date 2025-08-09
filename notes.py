#!/usr/bin/env python

import gi, os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class NoteTaker(Gtk.Window):
    def __init__(self):
        super().__init__(title="Notes")
        self.set_default_size(400, 300)
        self.connect("destroy", Gtk.main_quit)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Title")
        vbox.pack_start(self.title_entry, False, False, 0)

        self.textbuffer = Gtk.TextBuffer()
        textview = Gtk.TextView(buffer=self.textbuffer)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(textview)
        vbox.pack_start(scrolled, True, True, 0)

        button_box = Gtk.Box(spacing=6)
        vbox.pack_start(button_box, False, False, 0)

        save_btn = Gtk.Button(label="Save")
        save_btn.connect("clicked", self.save)
        button_box.pack_start(save_btn, True, True, 0)

        load_btn = Gtk.Button(label="Open")
        load_btn.connect("clicked", self.load)
        button_box.pack_start(load_btn, True, True, 0)

        self.show_all()
        textview.grab_focus()

    def save(self, _):
        dialog = Gtk.FileChooserDialog(title="Save", parent=self, action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        dialog.set_do_overwrite_confirmation(True)

        txt_filter = Gtk.FileFilter()
        txt_filter.set_name("Text files")
        txt_filter.add_pattern("*.txt")
        dialog.add_filter(txt_filter)

        all_filter = Gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")
        dialog.add_filter(all_filter)

        dialog.set_filter(all_filter)

        title = self.title_entry.get_text().strip()
        if title:
            if not title.endswith(".txt"):
                title += ".txt"
            dialog.set_current_name(title)

        if dialog.run() == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            start, end = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(start, end, True)
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)
                self.title_entry.set_text(os.path.splitext(os.path.basename(filename))[0])
            except Exception as e:
                self.show_error("Save error", str(e))
        dialog.destroy()

    def load(self, _):
        dialog = Gtk.FileChooserDialog(title="Open", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        txt_filter = Gtk.FileFilter()
        txt_filter.set_name("Text files")
        txt_filter.add_pattern("*.txt")
        dialog.add_filter(txt_filter)

        all_filter = Gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")
        dialog.add_filter(all_filter)

        dialog.set_filter(all_filter)

        if dialog.run() == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    self.textbuffer.set_text(f.read())
                self.title_entry.set_text(os.path.splitext(os.path.basename(filename))[0])
            except Exception as e:
                self.show_error("Load error", str(e))
        dialog.destroy()

    def show_error(self, title, message):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.OK, text=title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

def main():
    NoteTaker()
    Gtk.main()

if __name__ == "__main__":
    main()
