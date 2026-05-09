import win32com.shell.shellcon as shellcon
import win32com.shell.shell as shell
import ctypes
import win32api
import win32process
import win32gui
import win32con

from ctypes import wintypes

APPCOMMAND_VOLUME_MUTE = 0x80000
APPCOMMAND_VOLUME_DOWN = 0x90000
APPCOMMAND_VOLUME_UP = 0xA0000
WM_APPCOMMAND = 0x0319
APPCOMMAND_VOLUME_UP = 0xA0000
APPCOMMAND_VOLUME_DOWN = 0x90000

def set_volume(level):
    level = max(0, min(100, int(level)))
    hwnd = win32gui.GetForegroundWindow()
    
    # Сбрасываем в 0 (50 кликов по 2% вниз)
    for _ in range(50):
        win32gui.SendMessage(hwnd, WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_DOWN)
        
    # Поднимаем до нужного (1 клик = 2%)
    steps = level // 2
    for _ in range(steps):
        win32gui.SendMessage(hwnd, WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_UP)

def _send_volume_command(command):
    # Находим хендл любого окна (используем рабочий стол), чтобы отправить сигнал
    hwnd = win32gui.GetForegroundWindow()
    win32gui.SendMessage(hwnd, win32con.WM_APPCOMMAND, 0, command)

def volume_up():
    # Увеличить на шаг (обычно 2%)
    _send_volume_command(APPCOMMAND_VOLUME_UP)

def volume_down():
    # Уменьшить на шаг
    _send_volume_command(APPCOMMAND_VOLUME_DOWN)

def volume_mute():
    # Включить/Выключить звук (Toggle)
    _send_volume_command(APPCOMMAND_VOLUME_MUTE)

def get_user():
    # Получить имя текущего пользователя
    return win32api.GetUserName()

def get_computer_name():
    # Получить имя компьютера
    return win32api.GetComputerName()

def exit_prog(code=0):
    # Жесткий выход из программы через WinAPI
    win32api.ExitProcess(code)

def get_cwd():
    # Текущая рабочая директория
    return win32api.GetCurrentDirectory()

def set_cwd(path):
    # Смена рабочей директории
    win32api.SetCurrentDirectory(path)

def get_special_folder(folder_id):
    # folder_id можно взять из shellcon (CSIDL_DESKTOP, CSIDL_APPDATA и т.д.)
    return shell.SHGetFolderPath(0, folder_id, None, 0)

def get_uptime():
    # Сколько миллисекунд назад была загружена Windows
    ms = ctypes.windll.kernel32.GetTickCount64()
    return ms / 1000  # Возвращаем в секундах

def sleep(s):
    # WinAPI Sleep принимает миллисекунды
    ms = s * 1000
    ctypes.windll.kernel32.Sleep(int(ms))

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

def get_mem_info():
    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(stat)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    # Возвращаем кортеж: (Всего ГБ, Свободно ГБ, Загрузка %)
    return (
        round(stat.ullTotalPhys / (1024**3), 2), 
        round(stat.ullAvailPhys / (1024**3), 2), 
        stat.dwMemoryLoad
    )

def shutdown(text="Выключение через winframe"):
    # Мягкое выключение
    win32api.InitiateSystemShutdown(None, text, 30, True, False)

def restart(text="Перезагрузка через winframe"):
    # Перезагрузка
    win32api.InitiateSystemShutdown(None, text, 30, True, True)

def lock_workstation():
    # Заблокировать экран (Win + L)
    ctypes.windll.user32.LockWorkStation()

def get_screen_size():
    width = ctypes.windll.user32.GetSystemMetrics(0)  # SM_CXSCREEN
    height = ctypes.windll.user32.GetSystemMetrics(1) # SM_CYSCREEN
    return width, height

def get_windows_version():
    v = ctypes.windll.ntdll.rtlGetVersion # Работает точнее всего
    # Тут сложная структура, но можно просто дернуть через win32api
    return win32api.GetVersionEx()

def get_drives():
    drives = win32api.GetLogicalDriveStrings()
    return drives.split('\000')[:-1]

def get_mouse_pos():
    # Возвращает (x, y)
    return win32api.GetCursorPos()

def set_mouse_pos(x, y):
    win32api.SetCursorPos((x, y))

def set_high_priority():
    handle = win32api.GetCurrentProcess()
    # HIGH_PRIORITY_CLASS = 128
    win32process.SetPriorityClass(handle, 128)

def info(author="author", version="1.0.0", license="license", text="WINFRAME LIBRARY"):
    # Рисуем красивую рамку
    line = "═" * 40
    header = "║" + f" {text}   ".center(40) + "║"
    
    print(f"╔{line}╗")
    print(header)
    print(f"╠{line}╣")
    print(f"║ Author: {author.ljust(30)} ║")
    print(f"║ Version: {version.ljust(29)} ║")
    print(f"║ License: {license.ljust(29)} ║")
    print(f"╚{line}╝")

def is_admin():
    """Возвращает True, если программа запущена от имени администратора."""
    try:
        # Функция IsUserAnAdmin возвращает 1 (True) или 0 (False)
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        # Если что-то пошло не так (например, очень старая ОС), считаем, что прав нет
        return False
