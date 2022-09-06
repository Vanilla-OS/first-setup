pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
modelsdir = join_paths(pkgdatadir, 'vanilla_first_setup/models')

sources = [
  '__init__.py',
  'config.py',
  'preset.py',
]

install_data(sources, install_dir: modelsdir)