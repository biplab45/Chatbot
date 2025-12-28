import eel
import os
import webbrowser
from pytube import Search

# Initialize Eel
base_path = os.path.dirname(os.path.abspath(__file__))
eel.init(os.path.join(base_path, 'web'))

@eel.expose
def process_command_js(command):
    """This function processes the text sent from the mobile browser"""
    command = command.lower()
    print(f"Processing: {command}")
    
    if "open" in command:
        site = command.replace("open", "").strip()
        webbrowser.open(f"https://www.{site}.com")
        return f"Opening {site}"
    
    elif "play" in command:
        song = command.replace("play", "").replace("on youtube", "").strip()
        try:
            video = Search(song).results[0]
            webbrowser.open(video.watch_url)
            return f"Playing {song}"
        except:
            return "Video not found"
            
    return "I heard you, but I don't know that command."

# To work on mobile, we must use host='0.0.0.0'
# Replace 8080 with any port you like
eel.start('index.html', host='0.0.0.0', port=8080, size=(400, 600))
