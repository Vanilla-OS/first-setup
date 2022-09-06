pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'sugar_cubes')
gnome = import('gnome')

gnome.compile_resources('sugar-cubes',
  'sugar-cubes.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'sugar-cubes.in',
  output: 'sugar-cubes',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'sugar-cubes-processor.in',
  output: 'sugar-cubes-processor',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

subdir('utils')
subdir('models')

sugar_cubes_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(sugar_cubes_sources, install_dir: moduledir)