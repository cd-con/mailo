from mail import IMAP
import datetime
import webbrowser
import dearpygui.dearpygui as dpg

import random, variables

imap = IMAP("imap.yandex.ru", "", "")

def please_wait():
    with dpg.window(label="Ожидание...", id="wait_task",
                    height=150, width=250, pos=[100,100]):
        dpg.add_text("Подождите...\nИдёт кеширование...")

def sync():
    please_wait()
    task_started = datetime.datetime.now()
    variables.mails = imap.getMails("Inbox")
    dpg.delete_item("wait_task")
    print(f"Task 'GetMail' was completed in {datetime.datetime.now() - task_started}")

def open_mail(sender, app_data, user_data):
    window_id = random.randint(111, 999)
    please_wait()

    with dpg.window(label=f"Mail {window_id}", id=f"letter_window_{window_id}"):
        dpg.add_text("From user: " + user_data[1])
        dpg.add_text("Theme: " + user_data[2])
        if "!HTML" in user_data[3]:
            webbrowser.open(user_data[3][6::])
        else:
            dpg.add_text(user_data[3])
        dpg.delete_item("wait_task")


def open_box():
    please_wait()
    with dpg.window(label=variables.selected_folder, id=f"folder_{variables.selected_folder.replace(' ', '_') + str(random.randint(1111, 9999))}",
                    height=300, width=250,
                    pos=[200, 20]):
        print(variables.mails)
        for mail in variables.mails:
            dpg.add_text(mail[1])
            dpg.add_text("From: " + mail[2])
            dpg.add_button(label="Open mail", callback=open_mail, user_data=mail)
        dpg.delete_item("wait_task")


def settings():
    try:
        with dpg.window(label=f"Settings", id=f"settings_window"):
            print("e")
            dpg.add_text("Text")
    except Exception as _:
        dpg.focus_item("settings_window")


def folders_list():
    with dpg.window(label="Folders", id=f"folders_window_{random.randint(1111, 9999)}", height=400, width=200,
                    pos=[0, 20]):
        selected_folder = "Inbox"
        dpg.add_button(label="Inbox", callback=open_box)


with dpg.window(label="Mailo", id="main_window", height=300, width=400):
    with dpg.menu_bar():
        with dpg.menu(label="Почта"):
            dpg.add_menu_item(label="Открыть папки", callback=folders_list)
            with dpg.menu(label="Настройки"):
                dpg.add_menu_item(label="Синхронизировать сейчас", callback=sync)
                dpg.add_menu_item(label="Параметры", callback=settings)
        dpg.add_menu_item(label="О программе")
        folders_list()

with dpg.font_registry():
    with dpg.font(r"fonts\ru_alt.ttf", 18, default_font=True):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
