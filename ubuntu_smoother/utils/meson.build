pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
utilsdir = join_paths(pkgdatadir, 'sugar_cubes/utils')

sources = [
  '__init__.py',
  'checks.py',
  'apt.py',
  'flatpak.py',
  'snap.py',
  'configurator.py',
  'run_async.py',
  'processor.py',
]

install_data(sources, install_dir: utilsdir)