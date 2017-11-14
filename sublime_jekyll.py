import sublime
import sublime_plugin
import os
from datetime import datetime

SETTINGS = 'jekyll.sublime-settings'


class NewDraftCommand(sublime_plugin.WindowCommand):
    ''' Asks the user for the title of the new draft, and creates it '''
    def run(self):
        self.window.show_input_panel(
            'Título: ', '', self.input_done, None, None)

    def input_done(self, text):
        self.window.new_file()
        active_editor = self.window.active_view()
        author = sublime.load_settings(SETTINGS).get("author")
        if active_editor:
            active_editor.run_command(
                'insert', {'characters': '''---
layout: post
title: "{0}"
author: "{1}"
categories: {2}
comments: true
#images:

#  - url: /assets/img/
#    alt:
#    title:
---

'''.format(text, author)})
            active_editor.run_command()


class PublishDraftCommand(sublime_plugin.TextCommand):
    ''' Publish current draft '''
    def run(self, edit):
        date = '\ndate: {0}'.format(datetime.utcnow().strftime(
            '%Y-%m-%d %H:%M:%S'))
        self.view.insert(edit, self.view.text_point(5, 0) - 1, date)
        self.view.run_command('save')
        if len(self.view.file_name()) > 0:
            now = datetime.utcnow().strftime('%Y-%m-%d-')
            old_file = self.view.file_name()
            new_file = old_file.replace('/_drafts/', '/_posts/{0}'.format(now))
            os.rename(old_file, new_file)
            window = self.view.window()
            window.run_command("close_file")
            window.open_file(new_file)
