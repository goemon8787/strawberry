import pickle
import time

import chromedriver_binary
from selenium import webdriver

driver = webdriver.Chrome()
html = driver.get("https://www.data.jma.go.jp/gmd/risk/obsdl/index.php")
time.sleep(1)


# 各地域のid属性取得==========================================================
pr_list = []
prefecture = driver.find_elements_by_class_name("prefecture")
for pr in prefecture:
    pr = pr.get_attribute("id")
    pr_list.append(pr)
# ==========================================================================

# 各地域の観測地点名取得==========================================================
stname_list = []
for i in pr_list:
    # 順番に各地域へアクセス
    driver.find_element_by_xpath('//*[@id="{}"]'.format(i)).click()
    time.sleep(1)
    # その地域の観測地点情報の取得
    stations = driver.find_elements_by_xpath('//*[@class="station"]')
    for station in stations:
        station.click()  # 地点選択
        time.sleep(1)
        # 地点名取得
        stname = station.find_element_by_name("stname").get_attribute("value")
        stname_list.append(stname)
    # 全部選択し終わったらその地域から離れ、別の地域へ
    driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/input[1]"
    ).click()
    time.sleep(1)
# ==============================================================================

with open("./temp/pr_list.pkl", "wb") as f:
    pickle.dump(pr_list, f)

with open("./temp/area_list.pkl", "wb") as f:
    pickle.dump(stname_list, f)
