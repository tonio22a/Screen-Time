import ctypes
from ctypes import wintypes
import time
import storage

user32 = ctypes.windll.user32

running = True
work = storage.load()

def get_foreground_process_name():
    hwnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    handle = ctypes.windll.kernel32.OpenProcess(
        0x0400 | 0x0010, 
        False,
        pid.value
    )
    if not handle:
        return None

    buf = (ctypes.c_char * 260)()
    ctypes.windll.psapi.GetModuleBaseNameA(handle, None, buf, 260)
    ctypes.windll.kernel32.CloseHandle(handle)
    return buf.value.decode('utf-8', errors='ignore')


def track():
    while running:
        process = get_foreground_process_name()

        if process:
            work[process] = work.get(process, 0) + 1

        time.sleep(1)

def save_loop():
    while running:
        storage.save(work)
        time.sleep(25)
