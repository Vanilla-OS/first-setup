pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
dialogsdir = join_paths(pkgdatadir, 'vanilla_first_setup/dialogs')

sources = [
  '__init__.py',
  'subsystem.py',
]

install_data(sources, install_dir: dialogsdir)