# -*- coding: utf-8 -*-
import time
import pyautogui
import pyperclip

nextpage_coord = {'x':1744, 'y':896}
activate_window_coord = {'x':1851 , 'y':462 }

# nextpage_coord = {'x':1243, 'y':622}
# activate_window_coord = {'x':1320 , 'y':610 }

def switch_window():
    "ウィンドウを切り替える"
    pyautogui.hotkey("alt", "tab")

def del_tab():
    "chromeの現在のタブをタブを閉じる"
    pyautogui.hotkey("ctrl", "w")

def go_next_page():
    "次のページに行く"
    # 下までスクロール
    pyautogui.click(**activate_window_coord, clicks=1)
    time.sleep(1)
    pyautogui.scroll(-30000)
    pyautogui.scroll(-30000)
    time.sleep(0.5)

    # pyautogui.click(**activate_window_coord, clicks=1)
    # time.sleep(0.1)
    pyautogui.click(**nextpage_coord, clicks=1)
    # pyautogui.click(x=1243, y=622, clicks=1)
    # pyautogui.scroll(500, x=1320, y=610)

def get_html():
    "現在のページのhtmlを取得し、返す"
    "初期位置はハローワークのページを想定"
    # 現在のページのhtmlを表示
    # pyautogui.click(x=1320, y=610, clicks=1)
    pyautogui.click(**activate_window_coord, clicks=1)
    pyautogui.hotkey("ctrl", "u")
    time.sleep(4.5)

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
