import customtkinter as ctk
import func
import threading
import storage
import time
import pystray
from pystray import MenuItem as item
from PIL import Image
import os
import sys

app = ctk.CTk()
app.title("Screen Time")
app.after(200, lambda: app.iconbitmap(resource_path("logo.ico")))

# окно по центру
scaling = ctk.ScalingTracker().get_window_scaling(app)
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
app.geometry(f"490x590+{int(width/3*scaling)}+{int(height/3*scaling)}")

# память
d = 0
l = 0
b = 0

# функции

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def exit_action(icon, item):
    func.running = False
    icon.stop()
    app.after(0, app.destroy)

def show_action(icon, item):
    app.after(0, app.deiconify)

def hide_window():
    app.after(0, app.withdraw)

sorted_data = sorted(
    func.work.items(),
    key=lambda item: item[1],
    reverse=True
)


def change_theme_dark():
    ctk.set_appearance_mode("Dark")
    top1.configure(fg_color="#2b2b2b")

def change_theme_light():
    ctk.set_appearance_mode("Light")
    top1.configure(fg_color="#d6d6d6")

# интерфейс

tab_view = ctk.CTkTabview(app, width=450, height=500)
tab_view.place(x=20, y=20)

tab_1 = tab_view.add("Главная")
tab_2 = tab_view.add("Статистика")
tab_view.set("Главная")


text_base = ctk.CTkLabel(tab_1, text="Screen Time", font=ctk.CTkFont(f"Franklin Gothic Medium", size=25, weight="bold"))
text_base.place(x=20, y=20)

ct_d = ctk.CTkButton(tab_1, width=18, height=18, text="", command=change_theme_dark, fg_color="#4c4646", hover_color="#3a0303", corner_radius=100, border_color="white", border_width=0.3)
ct_d.place(x=320, y=25)
ct_l = ctk.CTkButton(tab_1, width=18, height=18, text="", command=change_theme_light, fg_color="white", hover_color="#e5e1e1", corner_radius=100, border_color="gray", border_width=0.3)
ct_l.place(x=350, y=25)

if sorted_data:
    top_text = f"🥇 Топ-1 по времени: {sorted_data[0]}"
else:
    top_text = "Пока нет данных"

top1 = ctk.CTkLabel(
    tab_1,
    text=top_text,
    font=ctk.CTkFont("Franklin Gothic Medium", size=17, weight="bold"),
    fg_color="#2b2b2b",
    corner_radius=10
)
top1.place(x=13, y=65)

def update_top():
    try:
        sorted_data = sorted(func.work.items(), key=lambda item: item[1], reverse=True)
        
        if sorted_data:
            app_name = sorted_data[0][0].replace('.exe', '') 
            app_time = sorted_data[0][1]
            top1.configure(text=f"🥇 Топ-1: {app_name} - {app_time} сек")
            
            top_5_text = "\n".join([f"{i+1}. {app.replace('.exe', '')}: {time} сек" 
                                   for i, (app, time) in enumerate(sorted_data[:5])])
            all_top.configure(text=top_5_text)
    except Exception as e:
        print(f"Ошибка в update_top: {e}")
    app.after(1000, update_top)

frame = ctk.CTkFrame(tab_2, corner_radius=12, width=370, height=370, fg_color=("gray85", "gray20"))
frame.place(x=35, y=15)

all_top_text = ctk.CTkLabel(
    frame,
    text="   ⏫ Все приложения",
    font=ctk.CTkFont("Franklin Gothic Medium", size=15, weight="bold"),
    text_color='yellow'
)
all_top_text.place(x=105, y=15)

all_top = ctk.CTkLabel(
    frame,
    text="\n".join([f"{i+1}. {app}: {time} сек" for i, (app, time) in enumerate(sorted_data[-100:])] if sorted_data else ["Нет данных"]),
    font=ctk.CTkFont("Franklin Gothic Medium", size=17, weight="bold"),
    corner_radius=10,
    anchor="nw"
)
all_top.place(x=15, y=50)

def create_tray_icon():
    image = Image.open(resource_path("logo.ico")) # Белый круг в центре

    menu = pystray.Menu(
        item("Показать", show_action),
        item('Выйти', exit_action)  # Пункт «Выход» для завершения приложения
    )

    # Создаём иконку и запускаем её
    icon = pystray.Icon("Screen Time", image, "Screen Time", menu)
    icon.run()

update_top()
thread1 = threading.Thread(target=create_tray_icon, daemon=True)
thread1.start()

thread2 = threading.Thread(target=func.track, daemon=True)
thread2.start()

thread3 = threading.Thread(target=func.save_loop, daemon=True)
thread3.start()
app.protocol("WM_DELETE_WINDOW", hide_window)
app.after(50, app.withdraw)
app.mainloop()


