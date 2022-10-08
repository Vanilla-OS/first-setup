<div align="center">
    <h1>Vanilla OS First Setup</h1>
    <p>This utility is meant to be used in <a href="https://github.com/vanilla-os">Vanilla OS</a> 
    as a first-setup wizard. It's purpose is to help the user to configure the 
    system to their needs, e.g. by configuring snap, flatpak, flathub, etc.</p>
    <img src="data/screenshot-1.png">
</div>


## Build
### Dependencies
- build-essential
- meson
- libadwaita-1-dev
- gettext
- desktop-file-utils

### Build
```bash
meson build
ninja -C build
```

### Install
```bash
sudo ninja -C build install
```

## Run
```bash
vanilla-first-setup
```

### Using custom recipes
Place a new recipe in `/etc/vanilla-first-setup/recipe.json` or launch the
utility with the `VANILLA_CUSTOM_RECIPE` environment variable set to the path
of the recipe.
