pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
utilsdir = join_paths(pkgdatadir, 'vanilla_first_setup/utils')

sources = [
  '__init__.py',
  'checks.py',
  'apt.py',
  'flatpak.py',
  'snap.py',
  'configurator.py',
  'run_async.py',
  'processor.py',
  'welcome_langs.py',
]

install_data(sources, install_dir: utilsdir)