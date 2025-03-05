pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
scriptsdir = join_paths(pkgdatadir, 'vanilla_first_setup/scripts')

sources = [
  'disable-lockscreen',
  'keyboard',
  'logout',
  'open-network-settings',
  'theme',
  'flatpak',
  'live-keyboard',
  'setup-flatpak-remote',
  'timezone',
  'hostname',
  'locale',
  'open-accessibility-settings',
  'setup-system',
  'user',
  'remove-first-setup-user',
  'remove-autostart-file',
]

install_data(sources, install_dir: scriptsdir)
