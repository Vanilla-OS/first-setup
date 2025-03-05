pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
viewsdir = join_paths(pkgdatadir, 'vanilla_first_setup/views')

sources = [
  '__init__.py',
  'applications.py',
  'conn_check.py',
  'done.py',
  'hostname.py',
  'keyboard.py',
  'language.py',
  'locations.py',
  'logout.py',
  'progress.py',
  'theme.py',
  'timezone.py',
  'user.py',
  'welcome_user.py',
  'welcome.py',
]

install_data(sources, install_dir: viewsdir)
