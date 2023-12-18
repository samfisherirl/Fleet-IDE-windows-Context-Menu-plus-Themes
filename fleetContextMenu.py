
import os
import winreg

# Define paths and menu text
menu_text = "Open with Fleet"
app_path = r"C:\Users\dower\AppData\Local\Programs\Fleet\Fleet.exe"
icon_path = r"C:\Users\dower\AppData\Local\Programs\Fleet\Fleet.ico"

def add_context_menu():
    """Adds a new context menu entry for folders."""

    # Open registry key
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"Directory\Background\shell", 0, winreg.KEY_WRITE)

    # Create subkey for the menu entry
    subkey = winreg.CreateKey(key, menu_text)

    # **Change:** Use f-string with curly braces for command
    winreg.SetValueEx(subkey, "command", 0, winreg.REG_SZ, f"\"{app_path}\" --dir \"%1\"")

    # Set default icon for the menu entry
    winreg.SetValueEx(subkey, "Icon", 0, winreg.REG_SZ, f"{app_path},0")

    # Close registry keys
    winreg.CloseKey(subkey)
    winreg.CloseKey(key)

def remove_context_menu():
    """Removes the existing context menu entry."""

    try:
        # Open registry key
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"Directory\Background\shell", 0, winreg.KEY_DELETE)

        # Delete the subkey for the menu entry
        winreg.DeleteKey(key, menu_text)

        # Close registry key
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass

try:
    # Check if existing entry needs to be removed
    if menu_text in os.listdir("HKEY_CLASSES_ROOT\\Directory\\Background\\shell"):
        remove_context_menu()
except:
    print("skipping remove")
# Add new context menu entry
add_context_menu()

print(f"Successfully added '{menu_text}' context menu entry for folders.")
