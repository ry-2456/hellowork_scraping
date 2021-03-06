# -*- coding: utf-8 -*-	
import re
import csv
import sys
import math
import pprint
from urllib import request
from bs4 import BeautifulSoup

from browser_manipulator import *

# フルタイム
# 全国・未経験可・ソフトウェア
# 職種　技術職 ソフトウェア開発技術者

added_comp_name = []

def get_searched_num(html):
    # 検索結果数を取得する
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find("div", class_="align_end")
    return int(res.div.div.span.string[:-1]) # 件という文字を取り除く

def show_length_and_elems(l):
    print("length: {}".format(len(l)))
    for i, e in enumerate(l):
        print(i, e)

def remove_extra_chars(s):
    # 文字列sから\n,\t,\sを取り除く
    return s.replace('　', '').replace('\t','').replace('\n','')

def scraping(html):
    # set BeautifulSoup インスタンスの作成
    soup = BeautifulSoup(html, "html.parser") 

    # 求人のhead, body, footを取得する
    kyujin_heads = soup.find_all("tr", attrs={"class", "kyujin_head"})
    kyujin_bodys = soup.find_all("tr", attrs={"class", "kyujin_body"})
    kyujin_foots = soup.find_all("tr", attrs={"class", "kyujin_foot"})

    # kyujin_footsを詳細ボタンを持っているものに絞り込む
    # kyujin_foots = [elem for elem in kyujin_foots if elem.find("a") is not None]

    occupations      = []    # 職種

    job_division     = []    # 求人区分
    companies        = []    # 会社の名前
    locations        = []    # 就業場所
    job_descriptions = []    # 仕事の内容
    emp_styles       = []    # 雇用形態
    payment          = []    # 賃金
    work_times       = []    # 就業時間
    day_off          = []    # 休日
    age_limits       = []    # 年齢
    offer_numbers    = []    # 求人番号


    # 職種を取得
    for head in kyujin_heads:
        occupations.append(head.find("tr").find_all("td")[1].div.string)
    # show_length_and_elems(occupations)
    

    # 会社名, 求人番号を取得
    for body in kyujin_bodys:
        body_row = body.find_all("tr")
        for i in range(len(body_row)):
            table_data = body_row[i].find_all("td")  # 全テーブルデータを取得
            # row_name = table_data[0].string          # データの名称を取得
            row_name = table_data[0].text          # データの名称を取得
            if row_name is None: continue

            if row_name == "求人区分":
                job_division.append(table_data[1].div.string)

            elif row_name == "事業所名":
                # companies.append(table_data[1].div.string)
                companies.append(table_data[1].div.text) # textはタグ内に含まれる文字列をつなぎ合わせて返す

            elif row_name == "就業場所":
                # locations.append(table_data[1].div.string)
                locations.append(remove_extra_chars(table_data[1].div.text))

            elif row_name == "仕事の内容":
                job_descriptions.append(table_data[1].div.text)

            elif row_name == "雇用形態":
                emp_styles.append(table_data[1].div.string)

            elif  "賃金" in row_name and "手当等" in row_name:
                # payment.append(table_data[1].div.text)
                payment.append(table_data[1].div.contents[3].string)

            elif row_name == "就業時間":
                work_times.append(remove_extra_chars(table_data[1].text))
                # work_times.append(table_data[1].text)
                # work_times.append(table_data[1].div.string)

            elif row_name == "休日":
                day_off.append(table_data[1].div.string)

            elif row_name == "年齢":
                # age_limits.append(table_data[1].contents)
                age_limits.append(remove_extra_chars(table_data[1].text))

            elif row_name == "求人番号":
                offer_numbers.append(table_data[1].div.string)
    
    c = len(companies)
    add_idx = []
    # 事業所名を公開していない会社と重複を省く
    for i, name in enumerate(companies):
        if "公開していません" not in name and name not in added_comp_name:
            add_idx.append(i)
            added_comp_name.append(name)

    info = []
    for l in  [companies, occupations, job_division,locations, job_descriptions, emp_styles, 
            payment, work_times, day_off, age_limits, offer_numbers]:
        l = [l[i] for i in range(c) if i in add_idx]
        info.append(l)

    return info
    # return [companies, 
    #         occupations, 
    #         job_division, 
    #         locations, 
    #         job_descriptions, 
    #         emp_styles, 
    #         payment, 
    #         work_times, 
    #         day_off, 
    #         age_limits,     
    #         offer_numbers]

def read_html(full_path):
    "full_pathで指定された、ファイルを読み込みその中身を返す"
    with open(full_path) as f:
        return f.read()

def write_joboffer_info(full_path, ll):
    # llはリストのリスト
    # full_pathで指定されたファイルに書き込む
    lines = []
    col_n = len(ll)     # 列の数
    row_n = len(ll[0])  # recordの数

    for i in range(row_n):
        record = [] 
        for j in range(col_n):
            record.append(ll[j][i])
        lines.append(record)

    with open(full_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(lines) 

def main(full_path):
    # vimの画面からブラウザへ
    # 検索件数を取得
    switch_window()
    html = get_html()
    del_tab()
    searched_num = get_searched_num(html)
    
    # 表示件数を自動で取得できるようにしよう
    for i in range(math.ceil(searched_num/50.0)):
        print("###### {} ######".format(i+1))
        # htmlを取得
        html = get_html()
        # htmlのページを閉じる
        del_tab()
        # スクレイピングを行う
        res = scraping(html)
        # csvファイルに書き込み
        write_joboffer_info(full_path, res)
        # 次のページヘ
        go_next_page()
        time.sleep(3)

def test(full_path):  
    for i in range(1):
        print("###### {} ######".format(i+1))
        html = get_html()
        # htmlのページを閉じる
        del_tab()
        # スクレイピングを行う
        res = scraping(html)
        get_searched_num(html)
        break
        # csvファイルに書き込み
        write_joboffer_info(full_path, res)
        # 次のページへ
        go_next_page()
        time.sleep(1)

if __name__ == "__main__":
    # file_path = "/home/t-rin/programming_project/brother_project/hello_work_scraping/"
    file_path = "./"
    file_name = input("input file name > ")
    # test(file_path + file_name)
    main(file_path + file_name)
