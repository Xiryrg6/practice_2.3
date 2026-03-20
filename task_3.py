import threading
import requests
import json
import time
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = 'resource/save.json'


def get_exchange_rates():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data['Valute']
    else:
        print("Ошибка при получении данных.")
        return {}


def load_groups():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = f.read().strip()
            if not data:
                return {}
            else:
                try:
                    json_data = json.loads(data)
                    if not json_data:
                        return {}
                    else:
                        return json_data
                except json.JSONDecodeError:
                    return {}
    return {}


def save_groups(groups):
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)


def show_all_currencies():
    currency_list = []

    for code, currency in currencies.items():
        currency_list.append(f"{code}: {currency['Name']} - {currency['Value']} RUB")

    currency_var = StringVar(value=currency_list)
    listbox_1["listvariable"] = currency_var


def searh_currency():
    code = entry_1.get()
    currency = currencies.get(code)
    if currency:
        label_1["text"] = f"{code}: {currency['Name']} - {currency['Value']} RUB"
    else:
        label_1["text"] = "Валюта с этим кодом не найдена."


def show_groups():
    groups_list = []
    if groups == {}:
        groups_list.append("Группы пока не созданы")
    else:
        for name, currencies in groups.items():
            groups_list.append(f"Группа: {name}")
            for code in currencies:
                groups_list.append(f"  - {code}")
            groups_list.append("")
    groups_var = StringVar(value=groups_list)

    listbox_2["listvariable"] = groups_var


def group_operation(groups, currencies, flag):
    name = entry_3.get()
    if name not in groups:
        label_3["text"] = "Такой группы нет"
    else:
        code = entry_4.get()
        if flag:
            if code not in currencies:
                label_3["text"] = "Неверный код валюты."
            else:
                if code in groups[name]:
                    label_3["text"] = "Эта валюта уже входит в группу."
                else:
                    groups[name].append(code)
                    save_groups(groups)
                    label_3["text"] = f"Валюта {code} добавлена в группу '{name}'."
        else:
            if code in groups[name]:
                groups[name].remove(code)
                save_groups(groups)
                label_3["text"] = f"Валюта {code} удалена из группы '{name}'"
            else:
                label_3["text"] = "Данная валюта не входит в эту группу"

    def task():
        time.sleep(2)
        label_3["text"] = ''
    threading.Thread(target=task).start()


def create_group():
    name = entry_2.get()
    if name in groups:
        label_2["text"] = "Эта группа уже существует"
    else:
        groups[name] = []
        save_groups(groups)
        label_2["text"] = f"Группа '{name}' создана."
    
    def task():
        time.sleep(2)
        label_2["text"] = ''
    threading.Thread(target=task).start()


def show_frame(frame):
    frame.tkraise()


currencies = get_exchange_rates()
groups = load_groups()

root = tk.Tk()
root.title("Курс валют")
root.geometry("400x300")
root.resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


frame_menu = ttk.Frame(root)
ttk.Label(frame_menu, text="Выберите действие", font=("", 14)).pack(pady=10)
ttk.Button(frame_menu, text="Посмотреть валюты", width=30, command=lambda:[show_frame(frame_show_all_currencies), show_all_currencies()]).pack(pady=3)
ttk.Button(frame_menu, text="Посмотреть группы", width=30, command=lambda:[show_frame(frame_show_groups), show_groups()]).pack(pady=3)
ttk.Button(frame_menu, text="Выход", width=30, command=lambda:root.destroy()).pack(pady=3)


frame_show_all_currencies = ttk.Frame(root)
frame_butt_1 = ttk.Frame(frame_show_all_currencies)

frame_butt_1.pack(fill='x')
frame_butt_1.columnconfigure(0, weight=1)
frame_butt_1.columnconfigure(1, weight=1)

ttk.Button(frame_butt_1, text="Обратно", command=lambda:show_frame(frame_menu)).grid(column=0, row=1, sticky="w")
ttk.Button(frame_butt_1, text="Просмотреть валюту по коду", command=lambda:show_frame(frame_view_currency)).grid(column=1, row=1, sticky='e')

ttk.Label(frame_show_all_currencies, text="Текущие обменные курсы всех валют", font=("", 14)).pack(pady=10)
listbox_1 = Listbox(frame_show_all_currencies)
listbox_1.pack(side=LEFT, fill=BOTH, expand=1)
scrollbar_1 = ttk.Scrollbar(frame_show_all_currencies, orient="vertical", command=listbox_1.yview)
scrollbar_1.pack(side="right", fill='y')
listbox_1["yscrollcommand"]=scrollbar_1.set


frame_view_currency = ttk.Frame(root)
ttk.Button(frame_view_currency, text="Обратно", command=lambda:[show_frame(frame_show_all_currencies), show_all_currencies()]).pack(anchor='nw')
ttk.Label(frame_view_currency, text="Введите код валюты", font=("", 12)).pack(pady=10)
entry_1 = ttk.Entry(frame_view_currency)
entry_1.pack(pady=10)
ttk.Button(frame_view_currency, text="Поиск", command=lambda:searh_currency()).pack(pady=5)
label_1 = ttk.Label(frame_view_currency)
label_1.pack(pady=10)


frame_show_groups = ttk.Frame(root)
frame_butt_2 = ttk.Frame(frame_show_groups)

frame_butt_2.pack(fill='x')
frame_butt_2.columnconfigure(0, weight=1)
frame_butt_2.columnconfigure(1, weight=1)
frame_butt_2.columnconfigure(2, weight=1)

ttk.Button(frame_butt_2, text="Обратно", command=lambda:show_frame(frame_menu)).grid(column=0, row=0, sticky='w')
ttk.Button(frame_butt_2, text="Изменить группу", command=lambda: show_frame(frame_add_or_delet_currency)).grid(column=1, row=0)
ttk.Button(frame_butt_2, text="Создать группу валют", command=lambda:show_frame(frame_create_group)).grid(column=2, row=0, sticky='e')

ttk.Label(frame_show_groups, text="Группы", font=("", 14)).pack(pady=10)
listbox_2 = Listbox(frame_show_groups)
listbox_2.pack(side=LEFT, fill=BOTH, expand=1)
scrollbar_2 = ttk.Scrollbar(frame_show_groups, orient="vertical", command=listbox_2.yview)
scrollbar_2.pack(side="right", fill='y')
listbox_2["yscrollcommand"]=scrollbar_2.set


frame_add_or_delet_currency = ttk.Frame()
ttk.Button(frame_add_or_delet_currency, text="Обратно", command=lambda:[show_frame(frame_show_groups), show_groups()]).pack(anchor='nw')
ttk.Label(frame_add_or_delet_currency, text="Введите группу", font=("", 12)).pack()
entry_3 = ttk.Entry(frame_add_or_delet_currency)
entry_3.pack(pady=10)
ttk.Label(frame_add_or_delet_currency, text="Введите номер валюты", font=("", 12)).pack()
entry_4 = ttk.Entry(frame_add_or_delet_currency)
entry_4.pack(pady=10)

frame_butt_3 = ttk.Frame(frame_add_or_delet_currency)
frame_butt_3.pack(fill="x", pady=10)
frame_butt_3.columnconfigure(0, weight=1)
frame_butt_3.columnconfigure(1, weight=1)

tk.Button(frame_butt_3, text="Добавить", bg="green", width=15, command=lambda: [group_operation(groups, currencies, True), entry_1.delete(0, last="end")]).grid(column=0, row=0)
tk.Button(frame_butt_3, text="Удалить", bg="red", width=15, command=lambda: [group_operation(groups, currencies, False), entry_1.delete(0, last="end")]).grid(column=1, row=0)
label_3 = ttk.Label(frame_add_or_delet_currency)
label_3.pack()


frame_create_group = ttk.Frame(root)
ttk.Button(frame_create_group, text="Обратно", command=lambda:[show_frame(frame_show_groups), show_groups()]).pack(anchor='nw')
ttk.Label(frame_create_group, text="Введите название группы", font=("", 12)).pack(pady=10)
entry_2 = ttk.Entry(frame_create_group)
entry_2.pack(pady=10)
ttk.Button(frame_create_group, text="Создать", command=lambda:create_group()).pack(pady=5)
label_2 = ttk.Label(frame_create_group)
label_2.pack(pady=10)


frames = [frame_menu,
           frame_show_all_currencies,
           frame_view_currency,
           frame_show_groups,
           frame_add_or_delet_currency,
           frame_create_group]
for frame in frames:
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(frame_menu)
root.mainloop()