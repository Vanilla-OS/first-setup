pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
coredir = join_paths(pkgdatadir, 'vanilla_first_setup/core')

sources = [
  '__init__.py',
  'languages.py',
  'keymaps.py',
  'timezones.py',
]

install_data(sources, install_dir: coredir)