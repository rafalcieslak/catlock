catlock
===

This tiny utility lets you quickly lock keyboard and mouse input. Unlike "Screen
lock" this tool does not hide the display.

The primary use of this script is to let your cat watch their favourite YouTube
videos without worrying that it might step on the keyboard and accidentally send
an e-mail to your boss.

Another use case is to play video games with a gamepad while your cat sleeps on
the keyboard.

## Usage

This script works only with X. It requires `python-xlib`. Install with `pip3
install python-xlib`.

To lock your keyboard & mouse, run the script:

```
./catlock.py
```

The script grabs both keyboard and mouse pointer. While it is running, all key
and button presses are ignored. When **Ctrl+Alt+K** is pressed, mouse and
keyboard are released (so your system is back to normal) and the script closes.

Additionally, for your convenience, on GNOME environments the script can install
a global shortcut that launches the script. Place the script in a permanent
path. Run:

```
./catlock.py install
```

From now on whenever you press **Ctrl+Alt+K** your system will enable
*catlock*. This is very convenient for quickly toggling between locked and
unlocked keyboard, without running the script manually.
