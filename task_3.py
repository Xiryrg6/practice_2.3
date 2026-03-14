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
    global listbox_1, scrollbar_1
    show_frame(frame_show_all_currencies)
    listbox_1.destroy()
    scrollbar_1.destroy()
    currency_list = []
    for code, currency in currencies.items():
        currency_list.append(f"{code}: {currency['Name']} - {currency['Value']} RUB")
    currency_var = StringVar(value=currency_list)
    listbox_1 = Listbox(frame_show_all_currencies, listvariable=currency_var)
    listbox_1.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar_1 = ttk.Scrollbar(frame_show_all_currencies, orient="vertical", command=listbox_1.yview)
    scrollbar_1.pack(side="right", fill='y')
    listbox_1["yscrollcommand"]=scrollbar_1.set


def view_currency():
    show_frame(frame_view_currency)

def searh():
    global label_1
    label_1.destroy()
    code = entry_1.get()
    currency = currencies.get(code)
    if currency:
        label_1 = ttk.Label(frame_view_currency, text=f"{code}: {currency['Name']} - {currency['Value']} RUB")
        label_1.pack(pady=15)
    else:
        label_1 = ttk.Label(frame_view_currency, text="Валюта с этим кодом не найдена.")
        label_1.pack(pady=15)


def create_group():
    show_frame(frame_create_group)

def create():
    global label_2
    label_2.destroy()
    name = entry_2.get()
    if name in groups:
        label_2 = ttk.Label(frame_create_group, text="Эта группа уже существует")
        label_2.pack(pady=15)
        return
    groups[name] = []
    save_groups(groups)
    label_2 = ttk.Label(frame_create_group, text=f"Группа '{name}' создана.")
    label_2.pack(pady=15)

def show_groups():
    global listbox_2, scrollbar_2
    show_frame(frame_show_groups)
    listbox_2.destroy()
    scrollbar_2.destroy()
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
    listbox_2 = Listbox(frame_show_groups, listvariable=groups_var)
    listbox_2.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar_2 = ttk.Scrollbar(frame_show_groups, orient="vertical", command=listbox_2.yview)
    scrollbar_2.pack(side="right", fill='y')
    listbox_2["yscrollcommand"]=scrollbar_2.set


def add_currency_to_group():
    show_frame(frame_add_currency_to_group)

def add(groups, currencies):
    global label_3
    label_3.destroy()
    name = entry_3.get()
    if name not in groups:
        label_3 = ttk.Label(frame_add_currency_to_group, text="Такой группы нет")
        label_3.pack()
        return
    code = entry_4.get()
    if code not in currencies:
        label_3 = ttk.Label(frame_add_currency_to_group, text="Неверный код валюты.")
        label_3.pack()
        return
    if code in groups[name]:
        label_3 = ttk.Label(frame_add_currency_to_group, text="Эта валюта уже входит в группу.")
        label_3.pack()
        return
    groups[name].append(code)
    save_groups(groups)
    label_3 = ttk.Label(frame_add_currency_to_group, text=f"Валюта {code} добавлена в группу '{name}'.")
    label_3.pack()


def remove_currency_from_group():
    show_frame(frame_remove_currency_from_group)

def remove(groups):
    global label_4
    label_4.destroy()
    name = entry_5.get()
    if name not in groups:
        label_4 = ttk.Label(frame_remove_currency_from_group, text="Нет такой группы.")
        label_4.pack()
        return
    code = entry_6.get()
    if code in groups[name]:
        groups[name].remove(code)
        save_groups(groups)
        label_4 = ttk.Label(frame_remove_currency_from_group, text=f"Валюта {code} удалена из группы '{name}'.")
        label_4.pack()
    else:
        label_4 = ttk.Label(frame_remove_currency_from_group, text="Данная валюта не входит в эту группу.")
        label_4.pack()

def menu():
    show_frame(frame_menu)


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
ttk.Button(frame_menu, text="Посмотреть все валюты", width=30, command=lambda:show_all_currencies()).pack(pady=3)
ttk.Button(frame_menu, text="Просмотреть валюту по коду", width=30, command=lambda:view_currency()).pack(pady=3)
ttk.Button(frame_menu, text="Создать группу валют", width=30, command=lambda:create_group()).pack(pady=3)
ttk.Button(frame_menu, text="Посмотреть все группы", width=30, command=lambda:show_groups()).pack(pady=3)
ttk.Button(frame_menu, text="Добавить валюту в группу", width=30, command=lambda:add_currency_to_group()).pack(pady=3)
ttk.Button(frame_menu, text="Удалить валюту из группы", width=30, command=lambda:remove_currency_from_group()).pack(pady=3)
ttk.Button(frame_menu, text="Выход", width=30, command=lambda:root.destroy()).pack(pady=3)


frame_show_all_currencies = ttk.Frame(root)
ttk.Button(frame_show_all_currencies, text="Обратно", command=lambda:menu()).pack(anchor='nw')
ttk.Label(frame_show_all_currencies, text="Текущие обменные курсы всех валют", font=("", 14)).pack(pady=10)
listbox_1 = Listbox(frame_show_all_currencies)
listbox_1.pack(side=LEFT, fill=BOTH, expand=1)
scrollbar_1 = ttk.Scrollbar(frame_show_all_currencies, orient="vertical", command=listbox_1.yview)
scrollbar_1.pack(side="right", fill='y')
listbox_1["yscrollcommand"]=scrollbar_1.set


frame_view_currency = ttk.Frame(root)
ttk.Button(frame_view_currency, text="Обратно", command=lambda:menu()).pack(anchor='nw')
ttk.Label(frame_view_currency, text="Введите код валюты", font=("", 12)).pack(pady=10)
entry_1 = ttk.Entry(frame_view_currency)
entry_1.pack(pady=10)
ttk.Button(frame_view_currency, text="Поиск", command=lambda:searh()).pack(pady=5)
label_1 = ttk.Label(frame_view_currency)


frame_create_group = ttk.Frame(root)
ttk.Button(frame_create_group, text="Обратно", command=lambda:menu()).pack(anchor='nw')
ttk.Label(frame_create_group, text="Введите название группы", font=("", 12)).pack(pady=10)
entry_2 = ttk.Entry(frame_create_group)
entry_2.pack(pady=10)
ttk.Button(frame_create_group, text="Создать", command=lambda:create()).pack(pady=5)
label_2 = ttk.Label(frame_create_group)


frame_show_groups = ttk.Frame(root)
ttk.Button(frame_show_groups, text="Обратно", command=lambda:menu()).pack(anchor='nw')
ttk.Label(frame_show_groups, text="Группы", font=("", 14)).pack(pady=10)
listbox_2 = Listbox(frame_show_groups)
listbox_2.pack(side=LEFT, fill=BOTH, expand=1)
scrollbar_2 = ttk.Scrollbar(frame_show_groups, orient="vertical", command=listbox_2.yview)
scrollbar_2.pack(side="right", fill='y')
listbox_2["yscrollcommand"]=scrollbar_2.set


frame_add_currency_to_group = ttk.Frame(root)
ttk.Button(frame_add_currency_to_group, text="Обратно", command=lambda:menu()).pack(anchor='nw')
ttk.Label(frame_add_currency_to_group, text="Введите название группы", font=("", 12)).pack(pady=10)
entry_3 = ttk.Entry(frame_add_currency_to_group)
entry_3.pack(pady=10)
ttk.Label(frame_add_currency_to_group, text="Введите код валюты", font=("", 12)).pack(pady=10)
entry_4 = ttk.Entry(frame_add_currency_to_group)
entry_4.pack(pady=10)
ttk.Button(frame_add_currency_to_group, text="Добавить", command=lambda: add(groups, currencies)).pack()
label_3 = ttk.Label(frame_add_currency_to_group)


frame_remove_currency_from_group = ttk.Frame(root)
ttk.Button(frame_remove_currency_from_group, text="Обратно", command=lambda:menu()).pack(anchor='nw')
ttk.Label(frame_remove_currency_from_group, text="Введите название группы", font=("", 12)).pack(pady=10)
entry_5 = ttk.Entry(frame_remove_currency_from_group)
entry_5.pack(pady=10)
ttk.Label(frame_remove_currency_from_group, text="Введите код валюты", font=("", 12)).pack(pady=10)
entry_6 = ttk.Entry(frame_remove_currency_from_group)
entry_6.pack(pady=10)
ttk.Button(frame_remove_currency_from_group, text="Удалить", command=lambda: remove(groups)).pack()
label_4 = ttk.Label(frame_remove_currency_from_group)


frames = [frame_menu,
           frame_show_all_currencies,
           frame_view_currency,
           frame_create_group,
           frame_show_groups,
           frame_add_currency_to_group,
           frame_remove_currency_from_group]
for frame in frames:
    frame.grid(row=0, column=0, sticky='nsew')

menu()
root.mainloop()