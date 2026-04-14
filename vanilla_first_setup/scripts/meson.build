pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
scriptsdir = join_paths(pkgdatadir, 'vanilla_first_setup/scripts')

sources = [
  'disable-lockscreen',
  'keyboard',
  'logout',
  'open-network-settings',
  'theme',
  'flatpak-install',
  'flatpak-uninstall',
  'live-keyboard',
  'setup-flatpak-remote',
  'timezone',
  'hostname',
  'locale',
  'open-accessibility-settings',
  'setup-system',
  'user',
  'remove-first-setup-user',
]

install_data(sources, install_dir: scriptsdir)
