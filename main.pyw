import eel
import os
import threading
import pystray
from PIL import Image, ImageDraw
import webbrowser

# --- Setup Paths ---
base_path = os.path.dirname(os.path.abspath(__file__))
eel.init(os.path.join(base_path, 'web'))

@eel.expose
def process_logic(command):
    """Processes text from the phone and returns the action to take"""
    command = command.lower()
    print(f"User said: {command}")

    if "open google" in command:
        return {"action": "open", "url": "https://www.google.com", "msg": "Opening Google"}
    
    elif "open youtube" in command:
        return {"action": "open", "url": "https://www.youtube.com", "msg": "Opening YouTube"}
    
    elif "play" in command:
        song = command.replace("play", "").strip()
        # We search via URL so it works on mobile browsers instantly
        url = f"https://www.youtube.com/results?search_query={song}"
        return {"action": "open", "url": url, "msg": f"Searching for {song}"}

    return {"action": "none", "msg": "I heard you, but I don't have a command for that."}

# --- System Tray Logic ---
def create_tray():
    image = Image.new('RGB', (64, 64), color=(15, 23, 42))
    d = ImageDraw.Draw(image)
    d.ellipse((10, 10, 54, 54), fill=(0, 210, 255))

    def on_quit(icon, item):
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("Open UI", lambda: threading.Thread(target=lambda: eel.start('index.html', size=(400, 600), block=False)).start()),
        pystray.MenuItem("Quit", on_quit)
    )
    icon = pystray.Icon("Jarvis", image, "Jarvis AI", menu)
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=create_tray, daemon=True).start()
    # host='0.0.0.0' allows your phone to connect via your laptop's IP
    eel.start('index.html', host='0.0.0.0', port=8080, size=(400, 600))
