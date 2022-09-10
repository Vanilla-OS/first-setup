application_id = 'io.github.vanilla-os.FirstSetup'

scalable_dir = join_paths('hicolor', 'scalable', 'apps')
install_data(
  join_paths(scalable_dir, ('@0@.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
)

symbolic_dir = join_paths('hicolor', 'symbolic')
install_data(
  join_paths(symbolic_dir, 'apps', ('@0@-symbolic.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir)
)

install_data(
    join_paths(symbolic_dir, 'actions', 'vanilla-container-terminal-symbolic.svg'),
    install_dir: join_paths(get_option('datadir'), 'icons', 'hicolor', 'scalable', 'actions')
)

install_data(
    join_paths(symbolic_dir, 'actions', 'vanilla-package-symbolic.svg'),
    install_dir: join_paths(get_option('datadir'), 'icons', 'hicolor', 'scalable', 'actions')
)

install_data(
    join_paths(symbolic_dir, 'actions', 'vanilla-puzzle-piece-symbolic.svg'),
    install_dir: join_paths(get_option('datadir'), 'icons', 'hicolor', 'scalable', 'actions')
)
