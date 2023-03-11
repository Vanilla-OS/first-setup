pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
defaultsdir = join_paths(pkgdatadir, 'vanilla_first_setup/defaults')

sources = [
  '__init__.py',
  'welcome.py',
  'theme.py',
  'user.py',
  'hostname.py',
  'applications.py',
  'conn_check.py'
]

install_data(sources, install_dir: defaultsdir)
