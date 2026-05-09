import ctypes
import win32gui
import win32con
import win32api

def _window_proc(hwnd, msg, wparam, lparam):
    global input_data, h_edit
    
    if msg == win32con.WM_COMMAND:
        # Если нажата кнопка (у нас её ID = 1)
        if wparam == 1: 
            # Забираем текст из поля ввода
            input_data = win32gui.GetWindowText(h_edit)
            win32gui.DestroyWindow(hwnd)
            
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0
        
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

def msg_box(text, title="Winframe", style=0):
    """
    Выводит стандартное окно Windows.
    Style: 0 - OK, 1 - OK/Cancel, 2 - Abort/Retry/Ignore, 4 - Yes/No
    Returns: ID нажатой кнопки (например, 6 - Yes, 7 - No)
    """
    # MessageBoxW для поддержки Unicode (русского языка)
    return ctypes.windll.user32.MessageBoxW(0, str(text), str(title), style)

def _create_window_frame(title, width, height):
    h_instance = win32api.GetModuleHandle(None)
    class_name = "WinframeWindow"

    # Регистрируем класс (один раз за запуск)
    wnd_class = win32gui.WNDCLASS()
    wnd_class.lpfnWndProc = _window_proc
    wnd_class.hInstance = h_instance
    wnd_class.hbrBackground = win32con.COLOR_BTNFACE + 1 # Системный цвет фона
    wnd_class.lpszClassName = class_name
    wnd_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    try:
        win32gui.RegisterClass(wnd_class)
    except: pass # Если класс уже есть

    # Создаем само окно
    hwnd = win32gui.CreateWindowEx(
        0, class_name, title,
        win32con.WS_OVERLAPPED | win32con.WS_CAPTION | win32con.WS_SYSMENU,
        win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
        width, height, 0, 0, h_instance, None
    )
    return hwnd

# 2. Функция создания формы ввода (наполняем каркас)
def input_form(title="Winframe", label="Введите текст:"):
    global h_edit, input_data
    input_data = None # Сброс данных перед открытием

    # Создаем каркас окна (ширина 350, высота 180)
    hwnd = _create_window_frame(title, 350, 180)
    h_instance = win32api.GetModuleHandle(None)

    # Используем системный шрифт по твоему запросу
    h_font = win32gui.GetStockObject(win32con.DEVICE_DEFAULT_FONT)

    # 1. Текст-подсказка
    h_static = win32gui.CreateWindowEx(0, "Static", label, 
        win32con.WS_CHILD | win32con.WS_VISIBLE,
        20, 20, 300, 20, hwnd, 0, h_instance, None)
    win32gui.SendMessage(h_static, win32con.WM_SETFONT, h_font, True)

    # 2. Поле ввода (записываем в глобальную h_edit, чтобы забрать текст в _window_proc)
    h_edit = win32gui.CreateWindowEx(win32con.WS_EX_CLIENTEDGE, "Edit", "", 
        win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.ES_AUTOHSCROLL,
        20, 45, 290, 25, hwnd, 100, h_instance, None)
    win32gui.SendMessage(h_edit, win32con.WM_SETFONT, h_font, True)

    # 3. Кнопка OK (ID = 1 для обработки в WM_COMMAND)
    h_btn = win32gui.CreateWindowEx(0, "Button", "OK", 
        win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_DEFPUSHBUTTON,
        120, 90, 100, 30, hwnd, 1, h_instance, None)
    win32gui.SendMessage(h_btn, win32con.WM_SETFONT, h_font, True)

    # Вывод окна на экран
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    
    # Запуск цикла сообщений (блокирует выполнение, пока окно не закроется)
    win32gui.PumpMessages()
    
    return input_data
        

def select_file(title="Выберите файл"):
    # Открывает стандартный проводник Windows для выбора файла
    fname, customfilter, flags = win32gui.GetOpenFileNameW(
        InitialDir='C:\\',
        Flags=win32con.OFN_EXPLORER,
        Title=title,
        Filter='All Files\0*.*\0Text Files\0*.txt\0',
        CustomFilter='Other\0*.*\0'
    )
    return fname
