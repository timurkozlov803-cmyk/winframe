import ctypes
import time

# Подгружаем системную библиотеку для работы с мультимедиа
winmm = ctypes.windll.winmm

def sound_open(path, alias="mysound"):
    # Команда: открыть файл под псевдонимом
    # Используем .encode('utf-8') так как WinAPI любит байты
    command = f'open "{path}" type mpegvideo alias {alias}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)

def sound_status(alias="mysound"):
    # Создаем буфер на 128 байт и заполняем его нулями
    buffer = ctypes.create_string_buffer(128)
    
    # Команда запроса режима (playing, stopped, paused)
    command = f'status {alias} mode'.encode('utf-8')
    
    # Вызываем функцию
    # Параметры: (команда, буфер_для_ответа, размер_буфера, хендл_коллбэка)
    winmm.mciSendStringA(command, buffer, 128, 0)
    
    # Превращаем байты в строку и убираем лишние пробелы/нули
    res = buffer.value.decode('utf-8').strip()
    return res

def sound_play(alias="mysound"):
    # Команда: играть с начала (или с текущего момента)
    command = f'play {alias}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)

    while sound_status(alias) == "playing":
        time.sleep(0.1)

def sound_pause(alias="mysound"):
    # Останавливает воспроизведение, но запоминает позицию
    command = f'pause {alias}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)

def sound_resume(alias="mysound"):
    # Продолжает играть с момента паузы
    command = f'resume {alias}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)

def sound_stop(alias="mysound"):
    # Полностью останавливает и сбрасывает на начало
    command = f'stop {alias}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)

def sound_close(alias="mysound"):
    # Выгружает файл из памяти (важно делать в конце!)
    command = f'close {alias}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)

def sound_rewind(s, alias="mysound"):
    ms = int(s * 1000)
    command = f'seek {alias} to {ms}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)
    winmm.mciSendStringA(f'play {alias}'.encode('utf-8'), None, 0, 0)

def sound_speed(speed=100, alias="mysound"):
    # Пересчитываем человеческие 100% в системные 1000 единиц
    mci_speed = int(speed * 10)
    
    # Команда set <alias> speed <value>
    command = f'set {alias} speed {mci_speed}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)

def sound_volume(level=100, alias="mysound"):
    # Уровень от 0 до 1000 в системе, так что множим на 10
    vol = int(level * 10)
    command = f'setaudio {alias} volume to {vol}'.encode('utf-8')
    winmm.mciSendStringA(command, None, 0, 0)

