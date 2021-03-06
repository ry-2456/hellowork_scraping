# -*- coding: utf-8 -*-	
import csv
import pprint
from urllib import request
from bs4 import BeautifulSoup

from browser_manipulator import *

# フルタイム
# 全国・未経験可・ソフトウェア
# 大阪兵庫.京都
# 職種　技術職 ソフトウェア開発技術者


def scraping(html):
    # set BeautifulSoup インスタンスの作成
    soup = BeautifulSoup(html, "html.parser") 

    # 求人のhead, body, footを取得する
    kyujin_heads = soup.find_all("tr", attrs={"class", "kyujin_head"})
    kyujin_bodys = soup.find_all("tr", attrs={"class", "kyujin_body"})
    kyujin_foots = soup.find_all("tr", attrs={"class", "kyujin_foot"})

    # kyujin_footsを詳細ボタンを持っているものに絞り込む
    kyujin_foots = [elem for elem in kyujin_foots if elem.find("a") is not None]

    occupations = []   # 職種
    companies = []     # 会社の名前
    offer_numbers = [] # 求人番号
    locations = []     # 勤務地

    # urls = []          # 会社のホームページURL

    # 職種を取得
    for head in kyujin_heads:
        occupations.append(head.find("tr").find_all("td")[1].div.string)

    # 会社名, 求人番号を取得
    for body in kyujin_bodys:
        body_row = body.find_all("tr")
        for i in range(len(body_row)):
            table_data = body_row[i].find_all("td")  # 全テーブルデータを取得
            row_name = table_data[0].string          # データの名称を取得
            if row_name is None: continue
            if row_name == "事業所名":
                companies.append(table_data[1].div.string)
            elif row_name == "求人番号":
                offer_numbers.append(table_data[1].div.string)

    # 事業所名を公開していない会社を取り除く
    for i, comp_name in enumerate(companies):
        if "公開していません" in comp_name:
            occupations[i] = None
            companies[i] = None
            offer_numbers[i] = None

    # Noneを削除
    occupations = [elem for elem in occupations if elem is not None]
    companies = [elem for elem in companies if elem is not None]
    offer_numbers = [elem for elem in offer_numbers if elem is not None]

    print("after")
    print("len(occupations): {}".format(len(occupations)))
    print("len(companies): {}".format(len(companies)))
    print("len(offer_numbers): {}".format(len(offer_numbers)))
    
    # return (companies, offer_numbers)
    return (companies, occupations, offer_numbers)

def read_html(full_path):
    "full_pathで指定された、ファイルを読み込みその中身を返す"
    with open(full_path) as f:
        return f.read()

def write_joboffer_info(full_path, companies, occupations, offer_numbers):
    # companies     :     会社の名前のリスト
    # offer_numbers : 求人番号
    lines = []
    # for c, o in zip(companies, offer_numbers):
    #     lines.append([c, o])

    for comp, occup, off_num in zip(companies, occupations, offer_numbers):
        lines.append([comp, occup, off_num])

    with open(full_path, mode="a") as f:
        writer = csv.writer(f)
        writer.writerows(lines) 

def main(full_path):
    # vimの画面からブラウザへ
    switch_window()
    for i in range(2426//30+1):
        print("###### {} ######".format(i+1))
        # html取得
        html = get_html()
        # htmlのページを閉じる
        del_tab()
        # スクレイピングを行う
        comp_names, occups, offer_nums = scraping(html)
        # csvファイルに書き込み
        write_joboffer_info(full_path, comp_names, occups, offer_nums)
        # 次のページヘ
        go_next_page()
        time.sleep(1)

def test(full_path):  
    for i in range(5):
        print("###### {} ######".format(i+1))
        html = get_html()
        # htmlのページを閉じる
        del_tab()
        # スクレイピングを行う
        comp_names, occups, offer_nums = scraping(html)
        # csvファイルに書き込み
        write_joboffer_info(full_path, comp_names, occups, offer_nums)
        # 次のページへ
        go_next_page()
        time.sleep(1)

if __name__ == "__main__":
    file_path = "/home/t-rin/brother_project/new_2020_0421/"
    file_name = "joboffer_info.csv"
    # test(file_path + file_name)
    main(file_path + file_name)
