from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

keyword = "渋谷 カフェ"
filename = "shibuya_cafes_ratings.csv"

driver = webdriver.Chrome()

try:
    driver.get("https://www.google.com/maps")
    time.sleep(3)

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    print("スクロールを開始します...")
    scrollable_div = driver.find_element(By.XPATH, '//div[@role="feed"]')
    
    # スクロール回数を5回に増やしてみましょう（もっと沢山取れます）
    for i in range(5):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(2)

    print("データ抽出を開始します...")

    # 【重要】店名単体ではなく、「お店のカード全体（枠）」をまず探します
    # Googleマップのリストの各項目は "Nv2PK" というクラス名が付いています
    cards = driver.find_elements(By.CLASS_NAME, "Nv2PK")

    print(f"合計 {len(cards)} 件のお店が見つかりました！")

    with open(filename, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["店名", "評価(星)"]) # ヘッダー

        for card in cards:
            try:
                # 1. カードの中から「店名」を探す
                title = card.find_element(By.CLASS_NAME, "fontHeadlineSmall").text
                
                # 2. カードの中から「評価（星）」を探す
                # 星の数字は "MW4etd" というクラス名についています
                try:
                    rating = card.find_element(By.CLASS_NAME, "MW4etd").text
                except:
                    rating = "-" # 評価がない店（新店など）の場合

                print(f"取得: {title} / ★{rating}")
                writer.writerow([title, rating])
                
            except Exception as e:
                # 何かエラーがあっても止まらずに次の店へ
                continue

    print(f"\n完了！ '{filename}' を確認してください。")

except Exception as e:
    print("エラー:", e)
finally:
    driver.quit()