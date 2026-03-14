import requests
import threading
import webbrowser
from tkinter import *
import tkinter as tk
from tkinter import ttk


def profile(user_data):
    show_frame(frame_profile)
    update_ui()
    ttk.Button(frame_profile, text="Обратно", command=lambda:show_frame(frame_menu)).pack(anchor='nw')
    ttk.Label(frame_profile, text=f"Профиль пользователя", font=("", 14)).pack(pady=10)
    frame = tk.Frame(frame_profile, bg="light gray", highlightbackground="black", highlightthickness=2)
    frame.pack()
    tk.Label(frame, bg="light gray", text=f"Логин: {user_data["login"]}").pack(anchor="nw")
    tk.Label(frame, bg="light gray", text=f"Имя: {user_data["name"]}").pack(anchor="nw")
    tk.Label(frame, bg="light gray", text=f"Репозиториев: {user_data["public_repos"]}").pack(anchor="nw")
    tk.Label(frame, bg="light gray", text=f"Обсуждений: {user_data["public_gists"]}").pack(anchor="nw")
    tk.Label(frame, bg="light gray", text=f"Подписчиков: {user_data["followers"]}").pack(anchor="nw")
    tk.Label(frame, bg="light gray", text=f"Подписок: {user_data["following"]}").pack(anchor="nw")
    lab = tk.Label(frame, bg="light gray", text=f"Профиль: {user_data["html_url"]}", fg="blue", cursor="hand2")
    lab.pack(anchor="nw")
    lab.bind("<Button-1>", callback)


def repos():
    show_frame(frame_repos)
    update_ui()

    frame = tk.Frame(frame_repos)
    frame.pack(fill=X)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=0)
    frame.columnconfigure(3, weight=0)
    ttk.Button(frame, text="Обратно", command=lambda:show_frame(frame_menu)).grid(row=0, column=0, sticky='w')
    ttk.Button(frame, text="Обновить", command=lambda: update(False)).grid(row=0, column=1, sticky='w')
    ttk.Button(frame, text="Поиск", command=lambda: update(True)).grid(row=0, column=3, sticky='e')
    entry_2 = ttk.Entry(frame)
    entry_2.grid(pady=2, row=0, column=2, sticky='e')

    ttk.Label(frame_repos, text=f"Репозитории", font=("", 14)).pack(pady=10)
    listbox_1 = Listbox(frame_repos)
    listbox_1.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar_1 = ttk.Scrollbar(frame_repos, orient="vertical", command=listbox_1.yview)
    scrollbar_1.pack(side="right", fill='y')
    listbox_1["yscrollcommand"]=scrollbar_1.set

    def update(flag):
        def task():
            nonlocal listbox_1, scrollbar_1, flag
            response = requests.get(f"https://api.github.com/users/{login}/repos")
            if response.status_code == 200:
                listbox_1.destroy()
                scrollbar_1.destroy()
                repos_data = response.json()
                lsit_repos = []
                search = entry_2.get()
                found = False
                if (not flag) and repos_data == {}:
                    lsit_repos.append("Репозитории отсутсвуют")
                else:
                    for repos in repos_data:
                        if flag:
                            if repos["name"] != search: continue
                        found = True
                        lsit_repos.append(f"Название: {repos['name']}")
                        lsit_repos.append(f"Просмотров: {repos['watchers_count']}")
                        lsit_repos.append(f"Язык: {repos['language']}")
                        lsit_repos.append(f"Видимость: {repos['visibility']}")
                        lsit_repos.append(f"Ветка по умолчанию: {repos['default_branch']}")
                        lsit_repos.append(f"Ссылка: {repos['html_url']}")
                        lsit_repos.append("")
                        if flag: break
                    if not found:
                        lsit_repos.append("Ничего не найденно")
                var_repos = StringVar(value=lsit_repos)
                listbox_1 = Listbox(frame_repos, listvariable=var_repos)
                listbox_1.pack(side=LEFT, fill=BOTH, expand=1)
                scrollbar_1 = ttk.Scrollbar(frame_repos, orient="vertical", command=listbox_1.yview)
                scrollbar_1.pack(side="right", fill='y')
                listbox_1["yscrollcommand"]=scrollbar_1.set
            else:
                print(f"Ошибка: {response.status_code}")
        threading.Thread(target=task).start()
    update(False)


def reg_login():
    def task():
        global label_1, login, response, user_data
        label_1.destroy()
        label_1 = ttk.Label(frame_login_user, text="Ожидайте")
        label_1.pack()
        login = entry_1.get()
        response = requests.get(f"https://api.github.com/users/{login}")
        if response.status_code == 200:
            user_data = response.json()
            show_frame(frame_menu)
        elif response.status_code == 404:
            label_1.destroy()
            label_1 = ttk.Label(frame_login_user, text="Пользователь не найден")
            label_1.pack()
        else:
            label_1.destroy()
            label_1 = ttk.Label(frame_login_user, text=f"Ошибка: {response.status_code}")
            label_1.pack()
    threading.Thread(target=task).start()


def callback(event):
    webbrowser.open_new(user_data["html_url"])


def show_frame(frame):
    frame.tkraise()


def update_ui():
    for widget in frame.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Просмотр GitHub")
root.geometry("400x300")
root.resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


frame_login_user = ttk.Frame(root)
ttk.Label(frame_login_user, text="Введите логин", font=("", 12)).pack(pady=10)
entry_1 = ttk.Entry(frame_login_user)
entry_1.pack()
ttk.Button(frame_login_user, text="Поиск", command=lambda: reg_login()).pack(pady=10)
label_1 = ttk.Label(frame_login_user)


frame_menu = ttk.Frame(root)
ttk.Label(frame_menu, text="Выберите действие", font=("", 14)).pack(pady=10)
ttk.Button(frame_menu, text="Просмотр профиля", width=30, command=lambda: profile(user_data)).pack(pady=3)
ttk.Button(frame_menu, text="Просмотр репозиториев", width=30, command=lambda: repos()).pack(pady=3)
ttk.Button(frame_menu, text="Выход", width=30, command=lambda: root.destroy()).pack(pady=3)

frame_profile = ttk.Frame(root)

frame_repos = ttk.Frame(root)

frames = [frame_menu,
          frame_login_user,
          frame_profile,
          frame_repos]
for frame in frames:
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(frame_login_user)
root.mainloop()