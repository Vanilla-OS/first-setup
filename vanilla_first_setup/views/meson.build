pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
viewsdir = join_paths(pkgdatadir, 'vanilla_first_setup/views')

sources = [
  '__init__.py',
  'done.py',
  'progress.py',
  'tour.py',
]

install_data(sources, install_dir: viewsdir)