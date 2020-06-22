# -*- coding: utf-8 -*-
import time
import pyautogui
import pyperclip

def switch_window():
    "ウィンドウを切り替える"
    pyautogui.hotkey("alt", "tab")

def del_tab():
    "chromeの現在のタブをタブを閉じる"
    pyautogui.hotkey("ctrl", "w")

def go_next_page():
    "次のページに行く"
    pyautogui.click(x=1320, y=610, clicks=1)
    pyautogui.hotkey("ctrl", "end")
    time.sleep(0.5)
    pyautogui.click(x=1243, y=617, clicks=1)
    # pyautogui.scroll(500, x=1320, y=610)

def get_html():
    "現在のページのhtmlを取得し、返す"
    "初期位置はハローワークのページを想定"
    # 現在のページのhtmlを表示
    pyautogui.click(x=1320, y=610, clicks=1)
    pyautogui.hotkey("ctrl", "u")
    time.sleep(4)

    # htmlの内容をクリップボードにコピーし、変数htmlに格納
    pyautogui.hotkey("ctrl", "a")
    time.sleep(1)
    pyautogui.keyDown("ctrlright")
    pyautogui.keyDown("c")
    time.sleep(1)
    pyautogui.keyUp("c")
    # pyautogui.press("c")
    pyautogui.keyUp("ctrlright")
    # pyautogui.hotkey("ctrl", "c")
    html = pyperclip.paste()
    return html

def where_am_I():
    # マウスの位置を返す ctrl+cで終了
    while True:
        pos = pyautogui.position()
        print("({x}, {y})".format(x=pos.x, y=pos.y))

if __name__ == "__main__":
    # where_i_am()
    switch_window()
    # html = get_html()
    go_next_page()
