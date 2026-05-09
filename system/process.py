import win32api
import win32process
import win32con
import win32gui

#Процесы
def open_file(path, argument=None, spec=None, mode=1):
    if mode == 1:
        md = win32con.SW_SHOWNORMAL
    elif mode == 2:
        md = win32con.SW_SHOWMAXIMIZED
    else:
        md = win32con.SW_HIDE

    win32api.ShellExecute(0, "open", path, argument, spec, md)

def get_process_exit_code(handle):
    # Узнать, работает ли еще процесс или с каким кодом он завершился
    return win32process.GetExitCodeProcess(handle)

def kill_process(nop):
    if str(nop).isdigit():
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, int(nop))
        win32api.TerminateProcess(handle, 0)
        win32api.CloseHandle(handle)

    elif str(nop).lower().endswith('.exe'):
        pids = win32process.EnumProcesses()
        for pid in pids:
            try:
                # Нам нужны права на чтение инфы и на убийство
                hProcess = win32api.OpenProcess(
                    win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ | win32con.PROCESS_TERMINATE, 
                    False, pid
                )
                # Берем имя процесса и сравниваем
                exe_path = win32process.GetModuleFileNameEx(hProcess, 0)
                if exe_path.lower().endswith(nop.lower()):
                    win32api.TerminateProcess(hProcess, 0)
                win32api.CloseHandle(hProcess)
            except:
                continue # Системные процессы просто скипаем

    else:
        hwnd = win32gui.FindWindow(None, nop)
        if hwnd:
            _, process_id = win32process.GetWindowThreadProcessId(hwnd)
            handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, process_id)
            win32api.TerminateProcess(handle, 0)
            win32api.CloseHandle(handle)
