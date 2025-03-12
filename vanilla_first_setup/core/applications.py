import requests
import threading

from gi.repository import GdkPixbuf, Gio, GLib

icon_url_cache = {}

def fetch_icon_url_from_id(id: str) -> str:
    if id in icon_url_cache:
        return icon_url_cache[id]

    response = requests.get(f'https://flathub.org/api/v2/appstream/{ id }')
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve icon for {id}, status code {response.status_code}")

    data = response.json()
    if "icon" not in data:
        raise ValueError(f"Server returned unexpected output for {id}: {data}")
    
    icon_url = data["icon"]

    icon_url_cache[id] = icon_url
    return icon_url

pixbuf_cache = {}

def fetch_pixbuf_from_url(url: str):
    if url in pixbuf_cache:
        return pixbuf_cache[url]

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to download {url}, server returned status code {response.status_code}")

    img_data = Gio.MemoryInputStream.new_from_data(response.content)
    pixbuf = GdkPixbuf.Pixbuf.new_from_stream(img_data, None)

    pixbuf_cache[url] = pixbuf
    return pixbuf

def set_app_icon_from_id_async(icon_widget, id: str):
    def fetch_icon_thread(widget, id: str):
        try:
            icon_url = fetch_icon_url_from_id(id)
            pixbuf = fetch_pixbuf_from_url(icon_url)
            GLib.idle_add(widget.set_from_pixbuf, pixbuf)
        except Exception as e:
            print(f"{e}")

    thread = threading.Thread(target=fetch_icon_thread, args=(icon_widget, id))
    thread.start()
