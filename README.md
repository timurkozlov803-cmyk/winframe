# winframe

Библиотека для работы с Windows API на Python.

## Структура

```
winframe/
├── core/      # Системные команды и утилиты
├── gui/       # Графический интерфейс
├── system/    # Работа с файлами, процессами и звуком
└── readme.txt # Документация
```

## Установка

Библиотека использует только встроенные модули Python и win32api, поэтому установка не требуется.

## Основы

```python
import winframe

# Импорт модулей
from winframe import core, gui, system
```

---

## Core Module

Системные команды и утилиты.

### Функции

#### set_volume(level)
Устанавливает громкость (0-100).

```python
core.set_volume(50)  # Установить громкость на 50%
```

#### volume_up()
Увеличивает громкость на шаг (2%).

```python
core.volume_up()
```

#### volume_down()
Уменьшает громкость на шаг (2%).

```python
core.volume_down()
```

#### volume_mute()
Переключает звук (вкл/выкл).

```python
core.volume_mute()
```

#### get_user()
Возвращает имя текущего пользователя.

```python
user = core.get_user()
```

#### get_computer_name()
Возвращает имя компьютера.

```python
computer = core.get_computer_name()
```

#### exit_prog(code=0)
Жесткий выход из программы.

```python
core.exit_prog(0)
```

#### get_cwd()
Возвращает текущую рабочую директорию.

```python
cwd = core.get_cwd()
```

#### set_cwd(path)
Меняет рабочую директорию.

```python
core.set_cwd("C:\\path\\to\\dir")
```

#### get_special_folder(folder_id)
Возвращает путь к специальной папке (CSIDL_DESKTOP, CSIDL_APPDATA и т.д.).

```python
import win32com.shell.shellcon as shellcon
desktop = core.get_special_folder(shellcon.CSIDL_DESKTOP)
```

#### get_uptime()
Возвращает время работы системы в секундах.

```python
uptime = core.get_uptime()
```

#### sleep(s)
Пауза на s секунд.

```python
core.sleep(1)  # Пауза на 1 секунду
```

#### get_mem_info()
Возвращает информацию о памяти: (Всего ГБ, Свободно ГБ, Загрузка %).

```python
total, free, load = core.get_mem_info()
```

#### shutdown(text="Выключение через winframe")
Мягкое выключение системы.

```python
core.shutdown("Выключение через winframe")
```

#### restart(text="Перезагрузка через winframe")
Перезагрузка системы.

```python
core.restart("Перезагрузка через winframe")
```

#### lock_workstation()
Блокирует экран (Win + L).

```python
core.lock_workstation()
```

#### get_screen_size()
Возвращает размер экрана: (ширина, высота).

```python
width, height = core.get_screen_size()
```

#### get_windows_version()
Возвращает версию Windows.

```python
version = core.get_windows_version()
```

#### get_drives()
Возвращает список дисков.

```python
drives = core.get_drives()
```

#### get_mouse_pos()
Возвращает позицию мыши: (x, y).

```python
x, y = core.get_mouse_pos()
```

#### set_mouse_pos(x, y)
Устанавливает позицию мыши.

```python
core.set_mouse_pos(100, 200)
```

#### set_high_priority()
Устанавливает высокий приоритет процесса.

```python
core.set_high_priority()
```

#### info(author="author", version="1.0.0", license="license", text="WINFRAME LIBRARY")
Выводит информацию о библиотеке.

```python
core.info(author="John Doe", version="1.0.0")
```

#### is_admin()
Возвращает True, если программа запущена от имени администратора.

```python
if core.is_admin():
    print("Запущено от администратора")
```

---

## GUI Module

Графический интерфейс с поддержкой CSS-стилей.

### Window

```python
from winframe.gui import ui

app = ui.Window("Моя программа", theme="dark")
app.geometry("600, 400")
```

#### Методы

##### geometry(size_str)
Устанавливает размеры окна.

```python
app.geometry("600, 400")
```

##### add_button(text, x, y, w=100, h=40, style=None, css=None, callback=None)
Добавляет кнопку.

**CSS свойства:**
- `background` / `background-color` - цвет фона
- `color` / `foreground` - цвет текста
- `border-radius` - радиус закругления углов
- `active-background` - цвет при наведении
- `width` - ширина
- `height` - высота

**Пример:**
```python
app.add_button(
    text="Нажми меня",
    x=20,
    y=20,
    css="""
        background: #32cd32;
        color: #ffffff;
        border-radius: 20px;
        active-background: #228b22;
        width: 150px;
        height: 50px;
    """,
    callback=lambda: print("Кнопка нажата")
)
```

##### add_label(text, x, y, w=None, h=None, style=None, css=None)
Добавляет текстовую метку.

**CSS свойства:**
- `color` / `foreground` - цвет текста
- `background` / `background-color` - цвет фона
- `font` - шрифт (например, "Arial 14 bold")
- `text-align` / `align` - выравнивание (left, center, right)
- `width` - ширина
- `height` - высота

**Пример:**
```python
app.add_label(
    text="Привет, мир!",
    x=20,
    y=80,
    css="""
        color: #ffffff;
        font: Arial 14 bold;
        text-align: center;
    """
)
```

##### add_entry(x, y, w=200, h=30, placeholder="", style=None, css=None, callback=None)
Добавляет поле ввода (одна строка).

**CSS свойства:**
- `background` / `background-color` - цвет фона
- `color` / `foreground` - цвет текста
- `border-radius` - радиус закругления
- `placeholder-color` - цвет плейсхолдера
- `font` - шрифт
- `width` - ширина
- `height` - высота

**Пример:**
```python
entry = app.add_entry(
    x=20,
    y=130,
    w=200,
    placeholder="Введите текст...",
    css="""
        background: #ffffff;
        color: #000000;
        border-radius: 10px;
        placeholder-color: #aaaaaa;
    """
)
```

##### add_text(x, y, w=200, h=100, placeholder="", style=None, css=None)
Добавляет многострочное поле ввода.

**CSS свойства:**
- `background` / `background-color` - цвет фона
- `color` / `foreground` - цвет текста
- `border-radius` - радиус закругления
- `placeholder-color` - цвет плейсхолдера
- `font` - шрифт
- `width` - ширина
- `height` - высота

**Пример:**
```python
text = app.add_text(
    x=20,
    y=180,
    w=300,
    h=100,
    placeholder="Введите многострочный текст...",
    css="""
        background: #ffffff;
        color: #000000;
        border-radius: 10px;
        placeholder-color: #aaaaaa;
    """
)
```

##### add_slider(x, y, w=200, h=30, min_val=0, max_val=100, value=50, style=None, css=None, callback=None, orientation="horizontal")
Добавляет ползунок.

**Параметры:**
- `orientation` - ориентация ("horizontal" или "vertical")

**CSS свойства:**
- `track-color` - цвет дорожки
- `thumb-color` - цвет ползунка
- `active-thumb-color` - цвет ползунка при наведении
- `border-radius` - радиус закругления
- `thumb-size` - размер ползунка
- `width` - ширина
- `height` - высота

**Пример:**
```python
slider = app.add_slider(
    x=20,
    y=300,
    w=200,
    min_val=0,
    max_val=100,
    value=50,
    css="""
        track-color: #cccccc;
        thumb-color: #32cd32;
        active-thumb-color: #228b22;
        border-radius: 15px;
        thumb-size: 20px;
    """,
    callback=lambda val: print(f"Значение: {val}")
)
```

##### add_switch(x, y, w=60, h=30, checked=False, style=None, css=None, callback=None)
Добавляет переключатель.

**CSS свойства:**
- `track-color-off` - цвет дорожки в выключенном состоянии
- `track-color-on` - цвет дорожки во включенном состоянии
- `thumb-color` - цвет ползунка
- `active-thumb-color` - цвет ползунка при наведении
- `border-radius` - радиус закругления
- `width` - ширина
- `height` - высота

**Пример:**
```python
switch = app.add_switch(
    x=20,
    y=350,
    checked=True,
    css="""
        track-color-off: #cccccc;
        track-color-on: #32cd32;
        thumb-color: #ffffff;
        active-thumb-color: #ffffff;
        border-radius: 15px;
    """,
    callback=lambda state: print(f"Переключатель: {'Вкл' if state else 'Выкл'}")
)
```

##### show()
Отображает окно.

```python
app.show()
```

### Boxes

Функции для работы с системными окнами.

#### msg_box(text, title="Winframe", style=0)
Выводит стандартное окно Windows.

**Style:**
- 0 - OK
- 1 - OK/Cancel
- 2 - Abort/Retry/Ignore
- 4 - Yes/No

**Возвращает:** ID нажатой кнопки (например, 6 - Yes, 7 - No)

```python
result = gui.msg_box("Текст сообщения", "Заголовок", 0)
```

#### input_form(title="Winframe", label="Введите текст:")
Открывает форму ввода текста.

**Возвращает:** Введенный текст или None

```python
text = gui.input_form("Ввод", "Введите ваше имя:")
```

#### select_file(title="Выберите файл")
Открывает стандартный проводник Windows для выбора файла.

**Возвращает:** Путь к файлу или пустая строка

```python
file_path = gui.select_file("Выберите файл")
```

---

## System Module

Работа с файлами, процессами и звуком.

### File

#### create_file(name="new_file.txt", path="", text="", mode=1, prive=0, code="utf-8")
Создает файл.

**Mode:**
- 1 - CREATE_ALWAYS (создать новый, перезаписать если есть)
- 2 - CREATE_NEW (создать только если нет)
- 3 - OPEN_ALWAYS (открыть или создать)
- 4 - OPEN_EXISTING (только открыть)

**Prive:** 0 - файл заблокирован для других

```python
system.file.create_file("test.txt", "", "Текст файла", 1, 0, "utf-8")
```

#### edit_file(name="new_file.txt", path="", text="", mode=1, move_to=0, code='utf-8')
Редактирует файл.

**Mode:**
- 1 - Записать с позиции move_to
- 2 - Добавить в конец
- 3 - Перезаписать всё

```python
system.file.edit_file("test.txt", "", "Новый текст", 1, 0, "utf-8")
```

#### read_file(name="new_file.txt", path="", size=1024, code='utf-8')
Читает файл.

```python
text = system.file.read_file("test.txt", "", 1024, "utf-8")
```

#### delete_file(name="new_file.txt", path="")
Удаляет файл.

```python
system.file.delete_file("test.txt", "")
```

#### rename_file(new_name, old_name="new_file.txt", path="")
Переименовывает файл.

```python
system.file.rename_file("new.txt", "old.txt", "")
```

### Process

#### open_file(path, argument=None, spec=None, mode=1)
Открывает файл или программу.

**Mode:**
- 1 - SW_SHOWNORMAL
- 2 - SW_SHOWMAXIMIZED
- 3 - SW_HIDE

```python
system.process.open_file("notepad.exe", "test.txt", None, 1)
```

#### get_process_exit_code(handle)
Получает код завершения процесса.

```python
code = system.process.get_process_exit_code(handle)
```

#### kill_process(nop)
Завершает процесс по PID или имени.

```python
system.process.kill_process(1234)  # По PID
system.process.kill_process("notepad.exe")  # По имени
```

### Sound

#### sound_open(path, alias="mysound")
Открывает аудиофайл.

```python
system.sound.open("music.mp3", "mysound")
```

#### sound_status(alias="mysound")
Возвращает статус воспроизведения (playing, stopped, paused).

```python
status = system.sound.status("mysound")
```

#### sound_play(alias="mysound")
Начинает воспроизведение.

```python
system.sound.play("mysound")
```

#### sound_pause(alias="mysound")
Ставит на паузу.

```python
system.sound.pause("mysound")
```

#### sound_resume(alias="mysound")
Продолжает воспроизведение.

```python
system.sound.resume("mysound")
```

#### sound_stop(alias="mysound")
Останавливает воспроизведение.

```python
system.sound.stop("mysound")
```

#### sound_close(alias="mysound")
Закрывает аудиофайл.

```python
system.sound.close("mysound")
```

#### sound_rewind(s, alias="mysound")
Перематывает на s секунд и начинает играть.

```python
system.sound.rewind(10, "mysound")  # Перемотать на 10 секунд
```

#### sound_speed(speed=100, alias="mysound")
Устанавливает скорость воспроизведения (100 = 100%).

```python
system.sound.speed(150, "mysound")  # 1.5x скорость
```

#### sound_volume(level=100, alias="mysound")
Устанавливает громкость (0-100).

```python
system.sound.volume(50, "mysound")  # 50% громкость
```

---

## Пример полного кода

```python
import winframe

# Импорт модулей
from winframe import core, gui, system

# Использование core
print(f"Пользователь: {core.get_user()}")
print(f"Память: {core.get_mem_info()}")

# Использование gui
app = gui.ui.Window("Моя программа", theme="dark")
app.geometry("600, 400")

app.add_button(
    text="Нажми меня",
    x=20,
    y=20,
    css="""
        background: #32cd32;
        color: #ffffff;
        border-radius: 20px;
        active-background: #228b22;
    """,
    callback=lambda: print("Кнопка нажата")
)

app.show()

# Использование system
system.file.create_file("test.txt", "", "Текст")
text = system.file.read_file("test.txt", "")
print(text)
system.sound.open("music.mp3", "mysound")
system.sound.play("mysound")
```

## Примечания

- Все виджеты GUI имеют закругленные углы
- CSS свойства имеют приоритет над параметрами методов
- Размеры можно задавать как в параметрах методов, так и через CSS свойства
- Ползунок поддерживает как горизонтальную, так и вертикальную ориентацию
- Переключатель возвращает True/False в callback
- Для работы библиотеки требуется модуль `pywin32`
