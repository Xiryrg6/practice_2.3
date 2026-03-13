import threading
import tkinter as tk
from tkinter import ttk
import requests

urls = ["https://github.com/", 
       "https://www.binance.com/en", 
       "https://tomtit.tomsk.ru/",
       "https://jsonplaceholder.typicode.com/",
       "https://moodle.tomtit-tomsk.ru/"]

result = []
progress = 0

def start_get():
    def task():
        global progress, result, progress_var
        result.clear()
        progress = 0
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, length=300, variable=progress_var, maximum=len(urls))
        progress_bar.pack(pady=10)
        
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                code = response.status_code
                match code:
                    case 200:
                        status = "-OK-200"
                    case 202:
                        status = "-Accepted-202"
                    case 204:
                        status = "-No_Content-204"
                    case 403:
                        status = "-Forbidden-403"
                    case 404:
                        status = "-Not_Found-404"
                    case 500:
                        status = "-Internal_Server-Error-500"
                    case 503:
                        status = "-Service_Unavailable-503"
                    case 504:
                        status = "-Gateway_Timeout-504"
                    case _:
                        status = f"-{code}"
                result.append(url + " " + status)
            except:
                result.append(url + " Ошибка")
            progress += 1
            root.after(0, update_ui)
        root.after(0, lambda: start_button.config(state='normal'))
        progress_bar.destroy()

    threading.Thread(target=task).start()

def update_ui():
    progress_var.set(progress)
    for widget in result_frame.winfo_children():
        widget.destroy()
    for res in result:
        lbl = ttk.Label(result_frame, text=res)
        lbl.pack()

root = tk.Tk()
root.title("Проверка API")
root.geometry("400x200")
root.resizable(False,False)

result_frame = ttk.Frame(root)
result_frame.pack(fill='both', expand=True)

start_button = ttk.Button(root, text="Start", command=lambda: [start_button.config(state='disabled'), start_get()])
start_button.pack(side="bottom", pady=10)

root.mainloop()