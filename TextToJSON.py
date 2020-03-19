import sublime_plugin
import sublime
import json
import os

class TexttojsonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.file_name().endswith('.ipynb'):
            return
        self.main(edit)

    def main(self, edit):
        if self.view.substr(sublime.Region(0, 1)) == "{":
            return
        if self.view.substr(sublime.Region(0, 2)) == '##':
            self.view.insert(edit, 0, '\n\n')
        fs = self.view.size()
        if fs > 7:
            if not self.view.substr(sublime.Region(fs-6, fs)) == '\n\n##\n\n':
                if not self.view.substr(sublime.Region(fs-7, fs)) == '## md\n\n':
                    self.view.insert(edit, fs, '\n\n##\n\n')
        normal_cells = self.view.find_all('\n\n##\n\n')
        markdown_cells = self.view.find_all('\n\n## md\n\n')
        all_cells = []
        for cell in normal_cells:
            all_cells.append((cell.a, cell.b, 0))
        for cell in markdown_cells:
            all_cells.append((cell.a, cell.b, 1))
        all_cells.sort(key=lambda x: x[0])
        all_cells_str = ''
        for idx, cell in enumerate(all_cells):
            last_cell = True if idx == len(all_cells) - 1 else False
            one_to_last = True if idx == len(all_cells) - 2 else False
            if not last_cell:
                next_cell = all_cells[idx + 1]
                region = sublime.Region(cell[1], next_cell[0])
                cell_source = self.view.substr(region)
                cell_source_final = ''
                lines = cell_source.split('\n')
                line_count = len(lines)
                for idx, line in enumerate(lines):
                    line = line.replace('\\', '\\\\')
                    line = line.replace('\"', '\\\"')
                    if idx == line_count - 1:
                        cell_source_final += '\"' + line + '\"'
                    else:
                        cell_source_final += '\"' + line + '\\n\",\n'
            else:
                continue  # file should end with \n\n##\n\n

            cell_type = 'code' if cell[2] == 0 else 'markdown'
            cell_st = '{\n'
            cell_st += '"cell_type": "' + cell_type + '",\n'
            if cell_type == 'code':
                cell_st += '"execution_count": null,\n'
                cell_st += '"outputs": [],\n'
            cell_st += '"metadata": {},\n'
            cell_st += '"source": [\n'
            cell_st += cell_source_final + '\n'
            cell_st += ']\n'
            if not one_to_last:
                cell_st += '},\n'
            else:
                cell_st += '}\n'
            all_cells_str += cell_st
        document = """{
 "cells": [
  """ + all_cells_str + """
         ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
"""
        self.view.replace(edit, sublime.Region(0, self.view.size()), document)
