import tkinter as tk
import re

class Window:
    def __init__(self, title="Winframe App", theme="system"):
        self.title = title
        self.theme = theme.lower()
        self.width, self.height = 400, 300
        
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Настройка темы
        if self.theme == "dark":
            self.root.configure(bg="#1e1e1e")
            self.default_btn_style = {
                "background": "#32cd32",
                "foreground": "#ffffff",
                "active_background": "#228b22",
                "border_radius": 20,
                "border_width": 0
            }
            self.bg_color = "#1e1e1e"
        else:
            self.root.configure(bg="#f0f0f0")
            self.default_btn_style = {
                "background": "#32cd32",
                "foreground": "#ffffff",
                "active_background": "#228b22",
                "border_radius": 20,
                "border_width": 0
            }
            self.bg_color = "#f0f0f0"
        
        self.buttons = []
        self.canvas_buttons = []
    
    def parse_css(self, css_text):
        """Парсит CSS текст и возвращает словарь стилей"""
        styles = {}
        # Ищем свойства вида property: value;
        pattern = r'([\w-]+)\s*:\s*([^;]+);?'
        matches = re.findall(pattern, css_text, re.IGNORECASE)
        
        for prop, value in matches:
            prop = prop.strip().lower()
            value = value.strip()
            
            if prop == 'background' or prop == 'background-color':
                styles['background'] = value
            elif prop == 'color' or prop == 'foreground':
                styles['foreground'] = value
            elif prop == 'border-radius':
                styles['border_radius'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'border-width':
                styles['border_width'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'active-background':
                styles['active_background'] = value
            elif prop == 'width':
                styles['width'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'height':
                styles['height'] = int(value.replace('px', '').replace(';', ''))
        
        return styles
    
    def geometry(self, size_str):
        try:
            w, h = size_str.replace(" ", "").split(",")
            self.width = int(w)
            self.height = int(h)
            self.root.geometry(f"{self.width}x{self.height}")
        except (ValueError, TypeError) as e:
            print(f"Ошибка при установке геометрии: {e}")
    
    def add_button(self, text, x, y, w=100, h=40, style=None, css=None, callback=None):
        """Добавляет кнопку с поддержкой CSS-подобного стиля"""
        btn_style = self.default_btn_style.copy()
        
        # Применяем CSS стиль если задан
        if css:
            btn_style.update(self.parse_css(css))
        
        # Применяем словарь стилей если задан
        if style:
            btn_style.update(style)
        
        # Используем размеры из CSS если заданы
        if 'width' in btn_style:
            w = btn_style['width']
        if 'height' in btn_style:
            h = btn_style['height']
        
        # Создаем Canvas для закругленной кнопки
        canvas = tk.Canvas(
            self.root,
            width=w,
            height=h,
            bg=self.bg_color,
            highlightthickness=0
        )
        canvas.place(x=x, y=y)
        
        # Рисуем закругленный прямоугольник (только углы закруглены)
        radius = btn_style["border_radius"]
        color = btn_style["background"]
        active_color = btn_style["active_background"]
        
        # Создаем закругленный прямоугольник из прямоугольников и кругов
        # 1. Центральный прямоугольник
        center_rect = canvas.create_rectangle(
            radius, 0, w - radius, h,
            fill=color,
            outline=color
        )
        
        # 2. Левый прямоугольник
        left_rect = canvas.create_rectangle(
            0, radius, radius, h - radius,
            fill=color,
            outline=color
        )
        
        # 3. Правый прямоугольник
        right_rect = canvas.create_rectangle(
            w - radius, radius, w, h - radius,
            fill=color,
            outline=color
        )
        
        # 4. Верхний прямоугольник
        top_rect = canvas.create_rectangle(
            radius, 0, w - radius, radius,
            fill=color,
            outline=color
        )
        
        # 5. Нижний прямоугольник
        bottom_rect = canvas.create_rectangle(
            radius, h - radius, w - radius, h,
            fill=color,
            outline=color
        )
        
        # 6. Четверти круга в углах
        # Левый верхний
        canvas.create_arc(0, 0, radius * 2, radius * 2, start=90, extent=90, fill=color, outline=color)
        # Правый верхний
        canvas.create_arc(w - radius * 2, 0, w, radius * 2, start=0, extent=90, fill=color, outline=color)
        # Правый нижний
        canvas.create_arc(w - radius * 2, h - radius * 2, w, h, start=270, extent=90, fill=color, outline=color)
        # Левый нижний
        canvas.create_arc(0, h - radius * 2, radius * 2, h, start=180, extent=90, fill=color, outline=color)
        
        # Добавляем текст кнопки
        text_id = canvas.create_text(
            w // 2,
            h // 2,
            text=text,
            fill=btn_style["foreground"],
            font=("Arial", 10, "bold")
        )
        
        # Сохраняем ID элементов для изменения цвета
        canvas.all_items = [center_rect, left_rect, right_rect, top_rect, bottom_rect]
        
        # Добавляем обработчики событий
        def on_enter(e):
            canvas.itemconfig(text_id, fill="#ffffff")
            for item in canvas.all_items:
                canvas.itemconfig(item, fill=active_color)
            # Обновляем углы
            for item in canvas.find_all():
                if canvas.type(item) == "arc":
                    canvas.itemconfig(item, fill=active_color)
        
        def on_leave(e):
            canvas.itemconfig(text_id, fill=btn_style["foreground"])
            for item in canvas.all_items:
                canvas.itemconfig(item, fill=color)
            # Обновляем углы
            for item in canvas.find_all():
                if canvas.type(item) == "arc":
                    canvas.itemconfig(item, fill=color)
        
        def on_click(e):
            if callback:
                callback()
        
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)
        
        self.canvas_buttons.append(canvas)
        return canvas
    
    def add_label(self, text, x, y, w=None, h=None, style=None, css=None):
        """Добавляет текстовую метку с поддержкой CSS-подобного стиля"""
        label_style = {
            "foreground": "#ffffff" if self.theme == "dark" else "#000000",
            "background": self.bg_color,
            "font": ("Arial", 10),
            "align": "center"
        }
        
        # Применяем CSS стиль если задан
        if css:
            label_style.update(self.parse_css_label(css))
        
        # Применяем словарь стилей если задан
        if style:
            label_style.update(style)
        
        # Используем размеры из CSS если заданы
        if 'width' in label_style:
            w = label_style['width']
        if 'height' in label_style:
            h = label_style['height']
        
        # Если размеры не заданы, вычисляем их автоматически
        if w is None or h is None:
            # Создаем временный canvas для измерения текста
            temp_canvas = tk.Canvas(self.root, width=1, height=1, bg=self.bg_color, highlightthickness=0)
            text_id = temp_canvas.create_text(0, 0, text=text, fill=label_style["foreground"], font=label_style["font"])
            bbox = temp_canvas.bbox(text_id)
            temp_canvas.destroy()
            
            if bbox:
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                w = w or text_width + 20
                h = h or text_height + 10
            else:
                w = w or 100
                h = h or 30
        
        # Создаем Canvas для метки
        canvas = tk.Canvas(
            self.root,
            width=w,
            height=h,
            bg=label_style["background"],
            highlightthickness=0
        )
        canvas.place(x=x, y=y)
        
        # Определяем выравнивание текста
        anchor = "center"
        if label_style["align"] == "left":
            anchor = "w"
        elif label_style["align"] == "right":
            anchor = "e"
        
        # Добавляем текст метки
        text_id = canvas.create_text(
            w // 2 if label_style["align"] == "center" else (10 if anchor == "w" else w - 10),
            h // 2,
            text=text,
            fill=label_style["foreground"],
            font=label_style["font"],
            anchor=anchor
        )
        
        self.canvas_buttons.append(canvas)
        return canvas
    
    def parse_css_label(self, css_text):
        """Парсит CSS текст для метки и возвращает словарь стилей"""
        styles = {}
        # Ищем свойства вида property: value;
        pattern = r'([\w-]+)\s*:\s*([^;]+);?'
        matches = re.findall(pattern, css_text, re.IGNORECASE)
        
        for prop, value in matches:
            prop = prop.strip().lower()
            value = value.strip()
            
            if prop == 'color' or prop == 'foreground':
                styles['foreground'] = value
            elif prop == 'background' or prop == 'background-color':
                styles['background'] = value
            elif prop == 'font':
                styles['font'] = value
            elif prop == 'text-align' or prop == 'align':
                styles['align'] = value
            elif prop == 'width':
                styles['width'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'height':
                styles['height'] = int(value.replace('px', '').replace(';', ''))
        
        return styles
    
    def add_entry(self, x, y, w=200, h=30, placeholder="", style=None, css=None, callback=None):
        """Добавляет поле ввода с поддержкой CSS-подобного стиля"""
        entry_style = {
            "background": "#ffffff",
            "foreground": "#000000",
            "placeholder_color": "#aaaaaa",
            "border_radius": 10,
            "border_width": 1,
            "font": ("Arial", 10)
        }
        
        # Применяем CSS стиль если задан
        if css:
            entry_style.update(self.parse_css_entry(css))
        
        # Применяем словарь стилей если задан
        if style:
            entry_style.update(style)
        
        # Используем размеры из CSS если заданы
        if 'width' in entry_style:
            w = entry_style['width']
        if 'height' in entry_style:
            h = entry_style['height']
        
        # Создаем Canvas для поля ввода
        canvas = tk.Canvas(
            self.root,
            width=w,
            height=h,
            bg=self.bg_color,
            highlightthickness=0
        )
        canvas.place(x=x, y=y)
        
        radius = entry_style["border_radius"]
        bg_color = entry_style["background"]
        
        # Рисуем закругленный прямоугольник
        center_rect = canvas.create_rectangle(
            radius, 0, w - radius, h,
            fill=bg_color,
            outline=bg_color
        )
        
        left_rect = canvas.create_rectangle(
            0, radius, radius, h - radius,
            fill=bg_color,
            outline=bg_color
        )
        
        right_rect = canvas.create_rectangle(
            w - radius, radius, w, h - radius,
            fill=bg_color,
            outline=bg_color
        )
        
        top_rect = canvas.create_rectangle(
            radius, 0, w - radius, radius,
            fill=bg_color,
            outline=bg_color
        )
        
        bottom_rect = canvas.create_rectangle(
            radius, h - radius, w - radius, h,
            fill=bg_color,
            outline=bg_color
        )
        
        # Четверти круга в углах
        canvas.create_arc(0, 0, radius * 2, radius * 2, start=90, extent=90, fill=bg_color, outline=bg_color)
        canvas.create_arc(w - radius * 2, 0, w, radius * 2, start=0, extent=90, fill=bg_color, outline=bg_color)
        canvas.create_arc(w - radius * 2, h - radius * 2, w, h, start=270, extent=90, fill=bg_color, outline=bg_color)
        canvas.create_arc(0, h - radius * 2, radius * 2, h, start=180, extent=90, fill=bg_color, outline=bg_color)
        
        # Создаем Entry внутри Canvas
        entry = tk.Entry(
            self.root,
            bg=bg_color,
            fg=entry_style["foreground"],
            font=entry_style["font"],
            relief="flat",
            borderwidth=0,
            insertbackground=entry_style["foreground"]
        )
        entry.place(x=x + 10, y=y + 5, width=w - 20, height=h - 10)
        
        # Добавляем placeholder
        if placeholder:
            entry.insert(0, placeholder)
            entry.placeholder = placeholder
            entry.placeholder_color = entry_style["placeholder_color"]
            entry.default_color = entry_style["foreground"]
            
            def on_focus_in(e):
                if entry.get() == entry.placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=entry.default_color)
            
            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, entry.placeholder)
                    entry.config(fg=entry.placeholder_color)
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
            on_focus_out(None)  # Установить placeholder при создании
        
        # Сохраняем ссылку на entry
        canvas.entry = entry
        canvas.all_items = [center_rect, left_rect, right_rect, top_rect, bottom_rect]
        
        self.canvas_buttons.append(canvas)
        return entry
    
    def parse_css_entry(self, css_text):
        """Парсит CSS текст для поля ввода и возвращает словарь стилей"""
        styles = {}
        # Ищем свойства вида property: value;
        pattern = r'([\w-]+)\s*:\s*([^;]+);?'
        matches = re.findall(pattern, css_text, re.IGNORECASE)
        
        for prop, value in matches:
            prop = prop.strip().lower()
            value = value.strip()
            
            if prop == 'background' or prop == 'background-color':
                styles['background'] = value
            elif prop == 'color' or prop == 'foreground':
                styles['foreground'] = value
            elif prop == 'border-radius':
                styles['border_radius'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'placeholder-color':
                styles['placeholder_color'] = value
            elif prop == 'font':
                styles['font'] = value
            elif prop == 'width':
                styles['width'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'height':
                styles['height'] = int(value.replace('px', '').replace(';', ''))
        
        return styles
    
    def add_text(self, x, y, w=200, h=100, placeholder="", style=None, css=None):
        """Добавляет многострочное поле ввода с поддержкой CSS-подобного стиля"""
        text_style = {
            "background": "#ffffff",
            "foreground": "#000000",
            "placeholder_color": "#aaaaaa",
            "border_radius": 10,
            "border_width": 1,
            "font": ("Arial", 10)
        }
        
        # Применяем CSS стиль если задан
        if css:
            text_style.update(self.parse_css_entry(css))
        
        # Применяем словарь стилей если задан
        if style:
            text_style.update(style)
        
        # Используем размеры из CSS если заданы
        if 'width' in text_style:
            w = text_style['width']
        if 'height' in text_style:
            h = text_style['height']
        
        # Создаем Canvas для многострочного поля ввода
        canvas = tk.Canvas(
            self.root,
            width=w,
            height=h,
            bg=self.bg_color,
            highlightthickness=0
        )
        canvas.place(x=x, y=y)
        
        radius = text_style["border_radius"]
        bg_color = text_style["background"]
        
        # Рисуем закругленный прямоугольник
        center_rect = canvas.create_rectangle(
            radius, 0, w - radius, h,
            fill=bg_color,
            outline=bg_color
        )
        
        left_rect = canvas.create_rectangle(
            0, radius, radius, h - radius,
            fill=bg_color,
            outline=bg_color
        )
        
        right_rect = canvas.create_rectangle(
            w - radius, radius, w, h - radius,
            fill=bg_color,
            outline=bg_color
        )
        
        top_rect = canvas.create_rectangle(
            radius, 0, w - radius, radius,
            fill=bg_color,
            outline=bg_color
        )
        
        bottom_rect = canvas.create_rectangle(
            radius, h - radius, w - radius, h,
            fill=bg_color,
            outline=bg_color
        )
        
        # Четверти круга в углах
        canvas.create_arc(0, 0, radius * 2, radius * 2, start=90, extent=90, fill=bg_color, outline=bg_color)
        canvas.create_arc(w - radius * 2, 0, w, radius * 2, start=0, extent=90, fill=bg_color, outline=bg_color)
        canvas.create_arc(w - radius * 2, h - radius * 2, w, h, start=270, extent=90, fill=bg_color, outline=bg_color)
        canvas.create_arc(0, h - radius * 2, radius * 2, h, start=180, extent=90, fill=bg_color, outline=bg_color)
        
        # Создаем Text внутри Canvas
        text = tk.Text(
            self.root,
            bg=bg_color,
            fg=text_style["foreground"],
            font=text_style["font"],
            relief="flat",
            borderwidth=0,
            insertbackground=text_style["foreground"],
            wrap="word"
        )
        text.place(x=x + 5, y=y + 5, width=w - 10, height=h - 10)
        
        # Добавляем placeholder
        if placeholder:
            text.insert("1.0", placeholder)
            text.placeholder = placeholder
            text.placeholder_color = text_style["placeholder_color"]
            text.default_color = text_style["foreground"]
            
            def on_focus_in(e):
                if text.get("1.0", "end-1c") == text.placeholder:
                    text.delete("1.0", tk.END)
                    text.config(fg=text.default_color)
            
            def on_focus_out(e):
                if not text.get("1.0", "end-1c"):
                    text.insert("1.0", text.placeholder)
                    text.config(fg=text.placeholder_color)
            
            text.bind("<FocusIn>", on_focus_in)
            text.bind("<FocusOut>", on_focus_out)
            on_focus_out(None)  # Установить placeholder при создании
        
        # Сохраняем ссылку на text
        canvas.text = text
        canvas.all_items = [center_rect, left_rect, right_rect, top_rect, bottom_rect]
        
        self.canvas_buttons.append(canvas)
        return text
    
    def add_slider(self, x, y, w=200, h=30, min_val=0, max_val=100, value=50, style=None, css=None, callback=None, orientation="horizontal"):
        """Добавляет ползунок с поддержкой CSS-подобного стиля"""
        slider_style = {
            "track_color": "#cccccc",
            "thumb_color": "#32cd32",
            "active_thumb_color": "#228b22",
            "border_radius": 15,
            "thumb_size": 20
        }
        
        # Применяем CSS стиль если задан
        if css:
            slider_style.update(self.parse_css_slider(css))
        
        # Применяем словарь стилей если задан
        if style:
            slider_style.update(style)
        
        # Используем размеры из CSS если заданы
        if 'width' in slider_style:
            w = slider_style['width']
        if 'height' in slider_style:
            h = slider_style['height']
        
        # Создаем Canvas для ползунка
        canvas = tk.Canvas(
            self.root,
            width=w,
            height=h,
            bg=self.bg_color,
            highlightthickness=0
        )
        canvas.place(x=x, y=y)
        
        track_color = slider_style["track_color"]
        thumb_color = slider_style["thumb_color"]
        active_thumb_color = slider_style["active_thumb_color"]
        radius = slider_style["border_radius"]
        thumb_size = slider_style["thumb_size"]
        
        # Рисуем дорожку ползунка
        if orientation == "horizontal":
            track_y = h // 2 - 3
            track_radius = radius
            track = canvas.create_polygon(
                [track_radius, track_y, w - track_radius, track_y, w, track_y + 3, w, track_y + 3,
                 w - track_radius, track_y + 6, track_radius, track_y + 6, 0, track_y + 3, 0, track_y + 3],
                fill=track_color,
                outline=track_color,
                smooth=True
            )
            
            # Рисуем ползунок
            thumb_x = (value - min_val) / (max_val - min_val) * (w - thumb_size)
            thumb = canvas.create_oval(
                thumb_x, h // 2 - thumb_size // 2,
                thumb_x + thumb_size, h // 2 + thumb_size // 2,
                fill=thumb_color,
                outline=thumb_color
            )
            
            # Сохраняем состояние
            canvas.min_val = min_val
            canvas.max_val = max_val
            canvas.value = value
            canvas.thumb = thumb
            canvas.track = track
            canvas.thumb_size = thumb_size
            canvas.w = w
            canvas.h = h
            canvas.orientation = "horizontal"
            canvas.callback = callback
            canvas.is_dragging = False
            
            # Добавляем обработчики событий
            def on_press(e):
                canvas.is_dragging = True
                on_move(e)
            
            def on_release(e):
                canvas.is_dragging = False
            
            def on_move(e):
                if canvas.is_dragging:
                    # Получаем позицию мыши относительно canvas
                    x_pos = max(0, min(e.x, w))
                    
                    # Вычисляем новое значение
                    range_val = max_val - min_val
                    value = min_val + (x_pos / (w - thumb_size)) * range_val
                    value = max(min_val, min(max_val, value))
                    
                    # Обновляем ползунок
                    thumb_x = (value - min_val) / (max_val - min_val) * (w - thumb_size)
                    canvas.coords(thumb, thumb_x, h // 2 - thumb_size // 2, thumb_x + thumb_size, h // 2 + thumb_size // 2)
                    canvas.value = value
                    
                    # Вызываем callback
                    if callback:
                        callback(value)
            
            canvas.bind("<ButtonPress-1>", on_press)
            canvas.bind("<ButtonRelease-1>", on_release)
            canvas.bind("<B1-Motion>", on_move)
        else:  # vertical
            track_x = w // 2 - 3
            track_radius = radius
            track = canvas.create_polygon(
                [track_x, track_radius, track_x + 3, 0, track_x + 3, h, track_x + 3, h,
                 track_x + 6, h - track_radius, track_x + 6, track_radius, track_x + 3, 0, track_x + 3, 0],
                fill=track_color,
                outline=track_color,
                smooth=True
            )
            
            # Рисуем ползунок
            thumb_y = h - ((value - min_val) / (max_val - min_val) * (h - thumb_size))
            thumb = canvas.create_oval(
                w // 2 - thumb_size // 2, thumb_y - thumb_size,
                w // 2 + thumb_size // 2, thumb_y,
                fill=thumb_color,
                outline=thumb_color
            )
            
            # Сохраняем состояние
            canvas.min_val = min_val
            canvas.max_val = max_val
            canvas.value = value
            canvas.thumb = thumb
            canvas.track = track
            canvas.thumb_size = thumb_size
            canvas.w = w
            canvas.h = h
            canvas.orientation = "vertical"
            canvas.callback = callback
            canvas.is_dragging = False
            
            # Добавляем обработчики событий
            def on_press(e):
                canvas.is_dragging = True
                on_move(e)
            
            def on_release(e):
                canvas.is_dragging = False
            
            def on_move(e):
                if canvas.is_dragging:
                    # Получаем позицию мыши относительно canvas
                    y_pos = max(0, min(e.y, h))
                    
                    # Вычисляем новое значение
                    range_val = max_val - min_val
                    value = min_val + ((h - y_pos) / (h - thumb_size)) * range_val
                    value = max(min_val, min(max_val, value))
                    
                    # Обновляем ползунок
                    thumb_y = h - ((value - min_val) / (max_val - min_val) * (h - thumb_size))
                    canvas.coords(thumb, w // 2 - thumb_size // 2, thumb_y - thumb_size, w // 2 + thumb_size // 2, thumb_y)
                    canvas.value = value
                    
                    # Вызываем callback
                    if callback:
                        callback(value)
            
            canvas.bind("<ButtonPress-1>", on_press)
            canvas.bind("<ButtonRelease-1>", on_release)
            canvas.bind("<B1-Motion>", on_move)
        
        self.canvas_buttons.append(canvas)
        return canvas
    
    def parse_css_slider(self, css_text):
        """Парсит CSS текст для ползунка и возвращает словарь стилей"""
        styles = {}
        # Ищем свойства вида property: value;
        pattern = r'([\w-]+)\s*:\s*([^;]+);?'
        matches = re.findall(pattern, css_text, re.IGNORECASE)
        
        for prop, value in matches:
            prop = prop.strip().lower()
            value = value.strip()
            
            if prop == 'track-color':
                styles['track_color'] = value
            elif prop == 'thumb-color':
                styles['thumb_color'] = value
            elif prop == 'active-thumb-color':
                styles['active_thumb_color'] = value
            elif prop == 'border-radius':
                styles['border_radius'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'thumb-size':
                styles['thumb_size'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'width':
                styles['width'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'height':
                styles['height'] = int(value.replace('px', '').replace(';', ''))
        
        return styles
    
    def add_switch(self, x, y, w=60, h=30, checked=False, style=None, css=None, callback=None):
        """Добавляет переключатель с поддержкой CSS-подобного стиля"""
        switch_style = {
            "track_color_off": "#cccccc",
            "track_color_on": "#32cd32",
            "thumb_color": "#ffffff",
            "active_thumb_color": "#ffffff",
            "border_radius": 15
        }
        
        # Применяем CSS стиль если задан
        if css:
            switch_style.update(self.parse_css_switch(css))
        
        # Применяем словарь стилей если задан
        if style:
            switch_style.update(style)
        
        # Используем размеры из CSS если заданы
        if 'width' in switch_style:
            w = switch_style['width']
        if 'height' in switch_style:
            h = switch_style['height']
        
        # Создаем Canvas для переключателя
        canvas = tk.Canvas(
            self.root,
            width=w,
            height=h,
            bg=self.bg_color,
            highlightthickness=0
        )
        canvas.place(x=x, y=y)
        
        track_color_off = switch_style["track_color_off"]
        track_color_on = switch_style["track_color_on"]
        thumb_color = switch_style["thumb_color"]
        active_thumb_color = switch_style["active_thumb_color"]
        radius = switch_style["border_radius"]
        thumb_size = h - 6
        
        # Рисуем дорожку переключателя
        track = canvas.create_oval(
            3, 3, w - 3, h - 3,
            fill=track_color_off if not checked else track_color_on,
            outline=track_color_off if not checked else track_color_on
        )
        
        # Рисуем ползунок
        thumb_x = 3 if not checked else w - thumb_size - 3
        thumb = canvas.create_oval(
            thumb_x, 3 + 3, thumb_x + thumb_size, 3 + thumb_size,
            fill=thumb_color,
            outline=thumb_color
        )
        
        # Сохраняем состояние
        canvas.checked = checked
        canvas.thumb = thumb
        canvas.track = track
        canvas.thumb_size = thumb_size
        canvas.w = w
        canvas.h = h
        canvas.callback = callback
        canvas.is_dragging = False
        
        # Добавляем обработчики событий
        def on_click(e):
            canvas.checked = not canvas.checked
            
            # Обновляем цвет дорожки
            canvas.itemconfig(track, fill=track_color_on if canvas.checked else track_color_off)
            canvas.itemconfig(track, outline=track_color_on if canvas.checked else track_color_off)
            
            # Обновляем позицию ползунка
            thumb_x = 3 if not canvas.checked else w - thumb_size - 3
            canvas.coords(thumb, thumb_x, 3 + 3, thumb_x + thumb_size, 3 + thumb_size)
            
            # Вызываем callback
            if callback:
                callback(canvas.checked)
        
        canvas.bind("<Button-1>", on_click)
        
        self.canvas_buttons.append(canvas)
        return canvas
    
    def parse_css_switch(self, css_text):
        """Парсит CSS текст для переключателя и возвращает словарь стилей"""
        styles = {}
        # Ищем свойства вида property: value;
        pattern = r'([\w-]+)\s*:\s*([^;]+);?'
        matches = re.findall(pattern, css_text, re.IGNORECASE)
        
        for prop, value in matches:
            prop = prop.strip().lower()
            value = value.strip()
            
            if prop == 'track-color-off':
                styles['track_color_off'] = value
            elif prop == 'track-color-on':
                styles['track_color_on'] = value
            elif prop == 'thumb-color':
                styles['thumb_color'] = value
            elif prop == 'active-thumb-color':
                styles['active_thumb_color'] = value
            elif prop == 'border-radius':
                styles['border_radius'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'width':
                styles['width'] = int(value.replace('px', '').replace(';', ''))
            elif prop == 'height':
                styles['height'] = int(value.replace('px', '').replace(';', ''))
        
        return styles
    
    def show(self):
        self.root.mainloop()
