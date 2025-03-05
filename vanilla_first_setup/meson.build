pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'vanilla_first_setup')
gnome = import('gnome')

gnome.compile_resources('vanilla-first-setup',
  'vanilla-first-setup.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: moduledir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('moduledir', moduledir)

configure_file(
  input: 'vanilla-first-setup.in',
  output: 'vanilla-first-setup',
  install_mode: 'rwxr-xr-x',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

subdir('core')
subdir('scripts')
subdir('views')

vanilla_first_setup_sources = [
  '__init__.py',
  'application.py',
  'main.py',
  'window.py',
  'dialog.py',
  'apps.json'
]

install_data(vanilla_first_setup_sources, install_dir: moduledir)
