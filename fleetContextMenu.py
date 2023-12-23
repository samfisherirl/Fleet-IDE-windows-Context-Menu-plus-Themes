from pathlib import Path
from os import getenv
import sys
import winreg
import ctypes
import time
import shutil

print(getenv('USERPROFILE') or getenv('HOME'))
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )


user = getenv('USERPROFILE') or getenv('HOME')
relative_themes = Path(__file__).parent / "themes"
fleet_folder = user / ".fleet" / "themes"
shutil.copy2(relative_themes, fleet_folder)

# Define paths and menu text
menu_text = "Open with Fleet"
appdata_local_path = getenv('LOCALAPPDATA') / 'Programs' 


# Specify the rest of the path to your executable
executable_path = 'Fleet\Fleet.exe'

# Combine the paths
app_path = appdata_local_path / executable_path

def add_context_menu(location):
    """Adds a new context menu entry for folders."""

    # Open registry key
    key_path = f"Directory\\{location}\\Open with Fleet"
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
    subkey = winreg.CreateKey(key, "command")

    # Set default values
    winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, f"\"{app_path}\",0")
    winreg.SetValueEx(key, None, 0, winreg.REG_SZ, menu_text)
    winreg.SetValueEx(subkey, None, 0, winreg.REG_SZ, f"\"{app_path}\" --dir \"%V\"")

    # Close registry keys
    winreg.CloseKey(subkey)
    winreg.CloseKey(key)

def remove_context_menu(location):
    """Removes the existing context menu entry."""
    key_path = f"Directory\\{location}\\Open with Fleet"

    try:
        # Delete the registry key and its subkeys
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
    except FileNotFoundError:
        print(f"Registry key not found: {key_path}")
    except Exception as e:
        print(f"Error removing context menu entry: {e}")

# Check if running as admin
if not is_admin():
    # Re-run the script as admin
    run_as_admin()
    sys.exit()

# Remove existing entries
remove_context_menu("Background\\shell")
remove_context_menu("shell")

# Add new context menu entry
add_context_menu("Background\\shell")
add_context_menu("shell")

print(f"Successfully added '{menu_text}' context menu entry for folders.")
time.sleep(3)
