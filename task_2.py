import psutil
import time
import threading
import tkinter as tk
from tkinter import ttk

def monitoring():
    def task():
        global result
        while True:
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            result = [f"CPU: {cpu_usage}%",
                      f"RAM: {memory.percent}% ({memory.used//1024//1024}MB / {memory.total//1024//1024}MB)",
                      f"Disk: {disk.percent}%"]
            root.after(0, update_ui)
            time.sleep(0.5)
    threading.Thread(target=task).start()

def update_ui():
    for widget in frame.winfo_children():
        widget.destroy()
    for res in result:
        lbl = ttk.Label(frame, text=res)
        lbl.pack(anchor='nw')

root = tk.Tk()
root.title("Мониторинг ресурсов")
root.geometry("200x60")
root.resizable(False, False)

frame = ttk.Frame(root)
frame.pack(fill='both', expand=True)

monitoring()

root.mainloop()