install_data(
    'firstsetup.desktop',
    install_dir: join_paths(get_option('datadir'), 'xsessions')
)

install_data(
    'org.vanillaos.FirstSetup.NewUser.desktop',
    install_dir: join_paths(get_option('datadir'), 'applications')
)

install_data(
    'firstsetup.json',
    install_dir: join_paths(get_option('datadir'), 'gnome-shell', 'modes')
)

install_data(
    'firstsetup.session',
    install_dir: join_paths(get_option('datadir'), 'gnome-session', 'sessions')
)

desktop_file = i18n.merge_file(
  input: 'org.vanillaos.FirstSetup.desktop.in',
  output: 'org.vanillaos.FirstSetup.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'org.vanillaos.FirstSetup.appdata.xml.in',
  output: 'org.vanillaos.FirstSetup.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('org.vanillaos.FirstSetup.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

subdir('icons')