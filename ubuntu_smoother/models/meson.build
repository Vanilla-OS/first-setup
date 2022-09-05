pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
modelsdir = join_paths(pkgdatadir, 'ubuntu_smoother/models')

sources = [
  '__init__.py',
  'config.py',
  'preset.py',
]

install_data(sources, install_dir: modelsdir)