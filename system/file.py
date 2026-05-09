import win32api
import win32con
import win32file

#Файлы
def create_file(name="new_file.txt", path="", text="", mode=1, prive=0, code="utf-8"):
    path = path + name
    if mode == 1:
        md = win32con.CREATE_ALWAYS
    elif mode == 2:
        md = win32con.CREATE_NEW
    elif mode == 3:
        md = win32con.OPEN_ALWAYS
    else:
        md = win32con.OPEN_EXISTING

    handle = win32file.CreateFile(
        path,                         # Имя файла
        win32con.GENERIC_WRITE,           # Доступ: на запись
        prive,                                # Совместный доступ: 0 — файл заблокирован для других
        None,                             # Атрибуты безопасности
        md,           # Режим: всегда создавать новый (перезапишет старый)
        win32con.FILE_ATTRIBUTE_NORMAL,   # Атрибуты файла
        None                              # Шаблон файла
    )

    if text != "":
        win32file.WriteFile(handle, text.encode(code))

    win32file.CloseHandle(handle)


def edit_file(name="new_file.txt", path="", text="", mode=1, move_to=0, code='utf-8'):
    path = path + name

    if mode == 1:
        handle = win32file.CreateFile(
            path,
            win32con.GENERIC_WRITE,
            0,
            None,
            win32con.OPEN_EXISTING, # Открыть только если файл уже есть
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )

        win32file.SetFilePointer(handle, move_to, win32con.FILE_BEGIN)
        win32file.WriteFile(handle, text.encode(code))

        win32file.CloseHandle(handle)

    elif mode == 2:
        handle = win32file.CreateFile(
            path,
            win32con.GENERIC_WRITE,
            0,
            None,
            win32con.OPEN_EXISTING, # Открыть только если файл уже есть
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )

        # Перемещаем указатель в конец файла
        # FILE_BEGIN - начало, FILE_CURRENT - текущая, FILE_END - конец
        win32file.SetFilePointer(handle, 0, win32con.FILE_END)

        # Записываем байты
        win32file.WriteFile(handle, text.encode(code))
        
        win32file.CloseHandle(handle)

    else:
        handle = win32file.CreateFile(
            path,
            win32con.GENERIC_WRITE,
            0,
            None,
            win32con.TRUNCATE_EXISTING, # Откроет и сотрет все содержимое
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )

        win32file.WriteFile(handle, text.encode(code))

        win32file.CloseHandle(handle)

def read_file(name="new_file.txt", path="", size=1024, code='utf-8'):
    path = path + name
    
    handle = win32file.CreateFile(
        path,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ, # Позволяем другим программам читать файл параллельно
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL,
        None
    )

    # ReadFile возвращает (код ошибки, считанные байты)
    hr, data = win32file.ReadFile(handle, size)
    
    win32file.CloseHandle(handle)
    return data.decode(code)

def delete_file(name="new_file.txt", path=""):
    full_path = path + name
    win32api.DeleteFile(full_path)

def rename_file(new_name, old_name="new_file.txt", path=""):
    old_path = path + old_name
    new_path = path + new_name
    # MoveFile также используется для переименования
    win32api.MoveFile(old_path, new_path)
