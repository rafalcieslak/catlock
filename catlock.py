#!/usr/bin/env python3

from Xlib.display import Display
from Xlib import X
import contextlib
import sys
import subprocess
import os
import ast

THIS_SCRIPT = os.path.realpath(__file__)
KEY_K = 45

disp = Display()
screen = disp.screen()
root = screen.root


@contextlib.contextmanager
def grab():
    root.grab_pointer(owner_events=True,
                      event_mask=0,
                      time=X.CurrentTime,
                      pointer_mode=X.GrabModeAsync,
                      keyboard_mode=X.GrabModeAsync,
                      confine_to=0,
                      cursor=0)
    root.grab_keyboard(owner_events=True,
                       time=X.CurrentTime,
                       pointer_mode=X.GrabModeAsync,
                       keyboard_mode=X.GrabModeAsync)
    yield
    disp.ungrab_keyboard(time=X.CurrentTime)
    disp.ungrab_pointer(time=X.CurrentTime)


# Grabs both keyboard and mouse pointer until Ctrl+Alt+K is pressed.
def catlock():
    with grab():
        while True:
            ev = root.display.next_event()
            if ev.type == X.KeyPress:
                if ev.state & X.ControlMask and ev.state & X.Mod1Mask:
                    if ev.detail == KEY_K:
                        return


# https://askubuntu.com/a/597414
def set_keyboard_shortcut(name, command, binding):
    # defining keys & strings to be used
    key = "org.gnome.settings-daemon.plugins.media-keys custom-keybindings"
    subkey = key.replace(" ", ".")[:-1]+":"
    item_s = "/"+key.replace(" ", "/").replace(".", "/")+"/"
    firstname = "custom"

    # get the current list of custom shortcuts
    current = subprocess.check_output(
        ["/bin/bash", "-c", "gsettings get " + key]
    ).decode("utf-8")
    current = ast.literal_eval(current)
    # make sure the additional keybinding mention is no duplicate
    n = 1
    while True:
        new = item_s+firstname+str(n)+"/"
        if new in current:
            n = n+1
        else:
            break
    # add the new keybinding to the list
    current.append(new)

    # create the shortcut, set the name, command and shortcut key
    cmd1 = "gsettings set {}{} name '{}'".format(subkey, new, name)
    cmd2 = "gsettings set {}{} command '{}'".format(subkey, new, command)
    cmd3 = "gsettings set {}{} binding '{}'".format(subkey, new, binding)
    cmd_ = 'gsettings set {} "{}"'.format(key, str(current))

    for cmd in [cmd1, cmd2, cmd3, cmd_]:
        subprocess.call(["/bin/bash", "-c", cmd])


# Installs a GNOME settings global keyboard shortcut that will run this script
# (and therefore lock keyboard/mouse) when Ctrl+Alt+K is pressed.
def install():
    print("Installing Ctrl+Alt+K shortcut")
    set_keyboard_shortcut("Cat Lock", THIS_SCRIPT, "<Ctrl><Alt>K")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        install()
    else:
        print("Press Ctrl+Alt+K to release grab.")
        catlock()
