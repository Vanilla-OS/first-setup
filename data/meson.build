install_data(
    'firstsetup-session.desktop',
    rename: 'firstsetup.desktop',
    install_dir: join_paths(get_option('datadir'), 'wayland-sessions')
)

install_data(
    'firstsetup-session-mode.json',
    rename: 'firstsetup.json',
    install_dir: join_paths(get_option('datadir'), 'gnome-shell', 'modes')
)

install_data(
    'firstsetup.session',
    install_dir: join_paths(get_option('datadir'), 'gnome-session', 'sessions')
)

install_data(
    'firstsetup.session.conf',
    install_dir: join_paths(get_option('prefix'), 'lib', 'systemd', 'user', 'gnome-session@firstsetup.target.d')
)

install_data(
    'org.vanillaos.FirstSetup.policy',
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'polkit-1', 'actions')
)

install_data(
    'org.vanillaos.FirstSetup.rules',
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'polkit-1', 'rules.d')
)

desktop_file = i18n.merge_file(
  input: 'org.vanillaos.FirstSetup.desktop.in',
  output: 'org.vanillaos.FirstSetup.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications'),
)

systemd_userunitdir = join_paths(get_option('prefix'), 'lib', 'systemd', 'user')

install_data(
  'org.vanillaos.FirstSetup.service',
  install_dir: systemd_userunitdir,
)

wantsdir = join_paths(get_option('prefix'), 'lib', 'systemd', 'user', 'gnome-session.target.wants')
meson.add_install_script(
  'sh', '-c',
  'install -d "$MESON_INSTALL_DESTDIR_PREFIX/' + wantsdir + '" && ' +
  'ln -sf ../org.vanillaos.FirstSetup.service "$MESON_INSTALL_DESTDIR_PREFIX/' + wantsdir + '/"'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

install_data(
  'remove-first-setup-user.service',
  install_dir: join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
)

install_data(
  'remove-first-setup-user',
  install_dir: join_paths(get_option('prefix'), 'libexec')
)

install_data(
  'firstsetup.conf',
  install_dir: join_paths(get_option('prefix'), 'lib', 'sysusers.d')
)

install_data(
  'firstsetup-tmpfiles.conf',
  install_dir: join_paths(get_option('prefix'), 'lib', 'tmpfiles.d')
)

systemd_systemunitdir = join_paths(get_option('prefix'), 'lib', 'systemd', 'system')

install_data(
  'first-setup-bootutil.service',
  install_dir: systemd_systemunitdir,
)

install_data(
  'first-setup-bootutil',
  install_dir: join_paths(get_option('prefix'), 'libexec'),
  install_mode: 'rwxr-xr-x',
)

multi_user_wantsdir = join_paths(systemd_systemunitdir, 'multi-user.target.wants')
meson.add_install_script(
  'sh', '-c',
  'install -d "$MESON_INSTALL_DESTDIR_PREFIX/' + multi_user_wantsdir + '" && ' +
  'ln -sf ../first-setup-bootutil.service "$MESON_INSTALL_DESTDIR_PREFIX/' + multi_user_wantsdir + '/"'
)

subdir('icons')
