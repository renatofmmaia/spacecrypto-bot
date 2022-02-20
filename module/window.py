import subprocess
from tkinter import * 
from tkinter.ttk import *
from enum import Enum

from module.platform import Platform, PlatformEnum


def get_windows(title:str):
    return (
        _get_linux_bombcrypto_windows(title)
        if Platform().get_platform() == PlatformEnum.LINUX
        else _get_bombcrypto_windows(title)
    )


def _get_linux_bombcrypto_windows(title):
    stdout = (
        subprocess.Popen(
            f"xdotool search --name '{title}'", shell=True, stdout=subprocess.PIPE
        )
        .communicate()[0]
        .decode("utf-8")
        .strip()
    )
    windows = stdout.split("\n")
    return [LinuxWindow(w) for w in windows]

def _get_bombcrypto_windows(title):
    import pygetwindow

    return [DefaultWindow(w) for w in pygetwindow.getWindowsWithTitle(title)]

def get_resolution():
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    
    if width == 1920 and height == 1080:
        return WindowsResolutionEnum.FULL_HD
    else:
        return WindowsResolutionEnum.NOT_SUPPORTED

class LinuxWindow:
    def __init__(self, window_id) -> None:
        self.window = window_id

    def activate(self):        
        subprocess.Popen(f"xdotool windowactivate {self.window}", shell=True)

class DefaultWindow:
    def __init__(self, window) -> None:
        self.window = window

    def activate(self):
        self.window.activate()
        
class WindowsResolutionEnum(Enum):
    FULL_HD = "1920x1080"
    NOT_SUPPORTED = "NOT_SUPPORTED"
