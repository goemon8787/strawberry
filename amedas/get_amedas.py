import os
import pickle
import shutil
import time

import chromedriver_binary
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select

if __name__ == "__main__":

    # スクレイピング
    driver = webdriver.Chrome()
    driver.get("https://www.data.jma.go.jp/gmd/risk/obsdl/index.php")
    time.sleep(1)

    # ダウンロードする地域
    select_list = [
        ["栃木", "宇都宮"],
        ["福岡", "福岡"],
        ["愛知", "名古屋"],
        ["静岡", "静岡"],
        ["長崎", "長崎"],
        ["宮崎", "宮崎"],
        ["佐賀", "佐賀"],
        ["熊本", "熊本"],
        ["宮城", "仙台"],
        ["香川", "香川"],
        ["北海道", "札幌"],
        ["秋田", "秋田"],
        ["青森", "青森"],
        ["群馬", "前橋"],
        ["長野", "長野"],
        ["広島", "広島"],
        ["岐阜", "岐阜"],
        ["徳島", "徳島"],
        ["山形", "山形"],
        ["茨城", "水戸"],
        ["福島", "福島"],
        ["大分", "大分"],
        ["石川", "金沢"],
        ["鹿児島", "鹿児島"],
        ["岩手", "盛岡"],
        ["山梨", "甲府"],
    ]
    select_list = [v[1] for v in select_list]

    # ダウンロードする期間の定義
    term = [
        ((2012, 1, 1), (2014, 12, 31)),
        ((2015, 1, 1), (2017, 12, 31)),
        ((2018, 1, 1), (2020, 12, 31)),
        ((2021, 1, 1), (2020, 10, 25)),
    ]

    with open(
        "/home/yamashitakeisuke/Documents/strawberry/amedas/temp/pr_list.pkl", "rb"
    ) as f:
        pr_list = pickle.load(f)

    # 地点を選ぶ
    driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/img[1]"
    ).click()
    time.sleep(1)

    # pr_list = pr_list[:10]
    for i in pr_list:
        flag = 0
        driver.find_element_by_xpath('//*[@id="{}"]'.format(i)).click()
        time.sleep(1)
        stations = driver.find_elements_by_xpath('//*[@class="station"]')
        time.sleep(1)
        for station in stations:
            station.click()
            time.sleep(1)
            stname = station.find_element_by_name("stname").get_attribute("value")
            # 選択中の地点がselect_listになければ、その地点をスキップする
            if not stname in select_list:
                print(stname + " skip")
            else:
                df = None

                # 項目を選ぶ
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/img[2]"
                ).click()
                time.sleep(1)

                # 日別値
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/ul/li[1]/a"
                ).click()
                time.sleep(1)

                # 気温
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/ul/li[1]/a"
                ).click()
                time.sleep(1)

                # 平均気温
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[1]/input"
                ).click()
                time.sleep(1)

                # 最高気温
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[4]/td[1]/input"
                ).click()
                time.sleep(1)

                # 最低気温
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr[5]/td[1]/input"
                ).click()
                time.sleep(1)

                # 降水
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/ul/li[2]/a"
                ).click()
                time.sleep(1)

                # 降水量の日合計
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[2]/table/tbody/tr[1]/td/input"
                ).click()
                time.sleep(1)

                # 日照/日射
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/ul/li[3]/a"
                ).click()
                time.sleep(1)

                # 日照時間
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[4]/table/tbody/tr[1]/td[1]/input"
                ).click()
                time.sleep(1)

                # 日合計全天日射量
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[4]/table/tbody/tr[1]/td[2]/input"
                ).click()
                time.sleep(1)

                # 湿度/気圧
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/ul/li[6]/a"
                ).click()
                time.sleep(1)

                # 日平均蒸気圧
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[6]/table/tbody/tr[1]/td[1]/input"
                ).click()
                time.sleep(1)

                # 日平均相対湿度
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[6]/table/tbody/tr[2]/td[1]/input"
                ).click()
                time.sleep(1)

                # 日平均現地気圧
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[6]/table/tbody/tr[1]/td[2]/input"
                ).click()
                time.sleep(1)

                # 日平均界面気圧
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[6]/table/tbody/tr[2]/td[2]/input"
                ).click()
                time.sleep(1)

                # 地域を選ぶ
                driver.find_element_by_id("stationButton").click()
                time.sleep(1)
                for k, t in enumerate(term):

                    # 期間を選ぶ
                    driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/img[3]"
                    ).click()
                    time.sleep(1)

                    # 連続した期間で表示する
                    driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/label/input"
                    ).click()
                    time.sleep(1)

                    # select 設定
                    select_temp = driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/select[1]"
                    )
                    start_select_year = Select(select_temp)
                    select_temp = driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/select[2]"
                    )
                    start_select_month = Select(select_temp)
                    select_temp = driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/select[3]"
                    )
                    start_select_day = Select(select_temp)

                    # 選択
                    start_select_year.select_by_visible_text(str(t[0][0]))
                    start_select_month.select_by_visible_text(str(t[0][1]))
                    start_select_day.select_by_visible_text(str(t[0][2]))

                    # select 設定
                    select_temp = driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[3]/select[1]"
                    )
                    end_select_year = Select(select_temp)
                    select_temp = driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[3]/select[2]"
                    )
                    end_select_month = Select(select_temp)
                    select_temp = driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[3]/select[3]"
                    )
                    end_select_day = Select(select_temp)

                    # 選択
                    end_select_year.select_by_visible_text(str(t[1][0]))
                    time.sleep(1)
                    end_select_month.select_by_visible_text(str(t[1][1]))
                    time.sleep(1)
                    end_select_day.select_by_visible_text(str(t[1][2]))
                    time.sleep(1)

                    driver.find_element_by_xpath(
                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/span/img"
                    ).click()

                    time.sleep(20)  # ダウンロードには多少時間がかかる
                    print(stname + " DL")

                    os.rename(
                        "/home/yamashitakeisuke/Downloads/data.csv",
                        "/home/yamashitakeisuke/Downloads/data" + str(k) + ".csv",
                    )
                    if not os.path.isdir(
                        "/home/yamashitakeisuke/Documents/strawberry/data/amedas/"
                        + str(i)
                    ):
                        os.mkdir(
                            "/home/yamashitakeisuke/Documents/strawberry/data/amedas/"
                            + str(i)
                        )
                    shutil.move(
                        "/home/yamashitakeisuke/Downloads/data" + str(k) + ".csv",
                        "/home/yamashitakeisuke/Documents/strawberry/data/amedas/"
                        + str(i),
                    )
                    flag = 1

            # 選択した地点を解除する
            driver.find_element_by_id("buttonDelAll").click()
            time.sleep(1)

            driver.find_element_by_id("stationButton").click()
            time.sleep(1)

            if flag:
                break

        # 他の都道府県を選ぶ
        driver.find_element_by_id("buttonSelectStation").click()
        time.sleep(1)
