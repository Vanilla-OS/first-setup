<div align="center">
    <img src="data/icons/hicolor/scalable/apps/org.vanillaos.FirstSetup.svg">
    <h1>Vanilla OS First Setup</h1>
    <p>This utility is meant to be used in <a href="https://github.com/vanilla-os">Vanilla OS</a>
    as a first-setup wizard. Its purpose is to help the user to configure the
    system to their needs, e.g. by configuring snap, flatpak, flathub, etc.</p>
    <hr />
    <a href="https://hosted.weblate.org/engage/vanilla-os/">
<img src="https://hosted.weblate.org/widgets/vanilla-os/-/first-setup/svg-badge.svg" alt="Translation status" />
</a>
    <br />
    <img src="data/screenshot-1.png">
</div>

## Build

### Build Dependencies
```bash
sudo apt install -y build-essential debhelper \
                    python3 meson \
                    libadwaita-1-dev gettext \
                    desktop-file-utils \
                    libjpeg-dev libnm-dev \
                    libnma-dev libnma-gtk4-dev \
                    ninja-build
```

### Runtime Dependencies
```bash
sudo apt install -y python3 python3-gi \
                    python3-tz libadwaita-1-0 \
                    gir1.2-gtk-4.0 gir1.2-adw-1 \
                    gir1.2-vte-3.91 libnm0 \
                    libnma0 libnma-gtk4-0
```

#### Optional Dependencies
```bash
sudo apt install python-requests # required for conn_check
sudo apt install gir1.2-gweather-4.0 # required for timezones
sudo apt install gir1.2-gnomedesktop-4.0 # required for languages, keyboard
sudo apt install gir1.2-nma4-1.0 # required for network
sudo apt install gir1.2-nm-1.0 # required for network
```

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
