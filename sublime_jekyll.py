import sublime
import sublime_plugin
import os
from datetime import datetime

class NewDraftCommand(sublime_plugin.WindowCommand):
    ''' Asks the user for the title of the new draft, and creates it '''
    def run(self):
        self.window.show_input_panel('Título: ', '', self.input_done, None, None)

    def input_done(self, text):
        self.window.new_file()
        active_editor = self.window.active_view()
        if active_editor:
            active_editor.run_command('insert',
                {'characters': '---\nlayout: post\ntitle: "{0}"\ncategories: \ncomments: true\n---\n\n'.format(text)})

class PublishDraftCommand(sublime_plugin.TextCommand):
    ''' Publish current draft, adding the date in UTC timezone '''
    def run(self, edit):
        date = '\ndate: {0}'.format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
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