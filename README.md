# sublime jupyter notebook viewer
A simple plugin for Sublime Text 3 which lets you view jupyter notebook files as flat python files.

# Requirements
To get the most out of this package it is recommended to install [sublime hooks](https://github.com/twolfson/sublime-hooks). This package can be installed by opening the Sublime Text terminal (`` CTRL+` ``)
```python
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/twolfson/sublime-hooks', 'hooks'], 'working_dir': path})
```

# Installation
The easiest way to install this package is to open the Subliem Text terminal (`` CTRL+` ``) and type the following command:
```python
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/nielsbos1996/sublime-jupyter-viewer', 'hooks'], 'working_dir': path})
```

# Set up
The easiest way to use this package is to adjust the Sublime settings so that it transforms the jupyter files to plain python files when a jupyter file is opened. When saving we want sublime to 1) transform the flat file to a valid jupyter file 2) save 3) convert back to a flat file. To do this go to preferences -> settings and change the User settings to
```json
{
	"ignored_packages":
	[
	],
	"on_pre_save_user": [
		{
			"command": "texttojson"
		}
	],
	"on_post_save_user": [
		{
			"command": "jsontotext"
		}
	],
	"on_load_user": [
		{
			"command": "jsontotext"
		}
	]
}

```

# Notes
Sublime always things that the .ipynb file contains unsaved changes. This is because the file is saved in json format and not plain text. When closing a file Sublime will ask if you want to save your changes. It is VERY IMPORTANT to click no, because by saving a file this way it won't be converted to a valid json file. 
