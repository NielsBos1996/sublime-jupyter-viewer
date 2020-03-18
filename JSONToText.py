import sublime_plugin
import sublime
import json
import os

class JsontotextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.file_name().endswith('.ipynb'):
            return
        self.main(edit)

    def main(self, edit):
        contents = self.view.substr(sublime.Region(0, self.view.size()))
        cells = json.loads(contents)['cells']
        cell_contents = []
        for cell in cells:
            cell_source = cell['source']
            cell_source = ''.join(cell_source)
            if cell['cell_type'] == 'code':
                cell_contents.append('\n\n##\n\n' + cell_source)
            else:
                cell_contents.append('\n\n## md\n\n' + cell_source)
        cell_contents = ''.join(cell_contents)
        self.view.replace(edit, sublime.Region(0, self.view.size()), cell_contents)
        self.view.set_syntax_file('Packages/Python/Python.sublime-syntax')
