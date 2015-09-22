# ES6 Import Manager

A simple ST3 plugin to reorder `require` and `import` statements in ES6 files. The plugin will reorder all `require` and `import` statements from the header of the specified file (all code until the body).

`require` statements will be left in their original order and moved to the top of the file.
`import` statements with no '/', taken as global modules, will be ordered alphabetically and placed at the top of the import list.
All other import statements will be ordered alphabetically, and folder groups will be separated by a newline character.

## Installation

Pull the git repository into `Packages/User`, then run `make install` to install the script.

## Usage

Either right click and select *Reorder imports*, or use `command-shift-r` to call the script. It will run on either the current selection, or the whole file if nothing is selected (recommended).
