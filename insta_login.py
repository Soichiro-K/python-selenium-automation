from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# --- ここを自分の情報に書き換えてください ---
USERNAME = "soich_dev_2025"
PASSWORD = "MyRealPassword123"
TARGET_TAG = "プログラミング学習" # 検索したいハッシュタグ
# ------------------------------------------

print("Instagramを起動します...")
driver = webdriver.Chrome()

try:
    # 1. ログインページを開く
    driver.get("https://www.instagram.com/")
    time.sleep(4) # 読み込み待ち（インスタは重いので長めに）

    # 2. ユーザーネーム入力
    # inputタグの name="username" を探す
    user_input = driver.find_element(By.NAME, "username")
    user_input.send_keys(USERNAME)
    
    # 3. パスワード入力
    pass_input = driver.find_element(By.NAME, "password")
    pass_input.send_keys(PASSWORD)
    
    # 4. Enterでログイン実行
    pass_input.send_keys(Keys.RETURN)
    
    print("ログイン試行中...")
    time.sleep(8) # ログイン処理待ち（ここも長めに）

    # --- ここからがテクニック ---
    # ログイン直後は「情報を保存しますか？」などのポップアップが出ますが、
    # 無視していきなり「ハッシュタグのページ」にURLで移動してしまいます。
    # これでポップアップ処理をサボることができます。

    tag_url = f"https://www.instagram.com/explore/tags/{TARGET_TAG}/"
    print(f"ハッシュタグ #{TARGET_TAG} のページへ移動します...")
    driver.get(tag_url)
    time.sleep(5)

    # 投稿の数を取得してみる（metaタグなどから）
    # または、表示されている画像のリンクを取得してみる
    
    print("表示されている投稿のリンクを取得します...")
    # インスタの投稿リンクは aタグの中に "/p/" が含まれています
    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
    
    for link in links[:5]: # 最初の5件だけ表示
        url = link.get_attribute("href")
        print(f"投稿URL: {url}")

    print("\n成功！Instagramの自動操作に成功しました。")
    time.sleep(10)

except Exception as e:
    print("エラーが発生しました:", e)

finally:
    driver.quit()