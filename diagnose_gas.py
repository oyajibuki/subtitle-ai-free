import urllib.request
import json
import ssl
import sys
import time

# あなたの実際のGASデプロイURLに書き換えてください
# もし [デプロイ] > [デプロイを管理] で新しいURLが発行されていたら、それに差し替えてください
GAS_URL = "https://script.google.com/macros/s/AKfycbw-GQUSSCTIbSRLMhaItLX6GZSi0iemw5Vaxo0oKB4Rg9OOf1xJ4UEBJHczY7-3LWPj_Q/exec"

def diagnose():
    print("=== AI Subtitle GAS 診断ツール ===")
    print(f"ターゲットURL: {GAS_URL}")
    email = "oyajibuki@gmail.com"
    
    # 1. POST (ライセンス発行) のテスト
    print("\n[1/2] ライセンス発行テスト (POST) を開始します...")
    payload = {
        "type": "checkout.session.completed",
        "data": {"object": {"id": f"diag_{int(time.time())}", "customer_details": {"email": email}}}
    }
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(GAS_URL, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            res_body = response.read().decode('utf-8')
            print(f"ステータスコード: {response.getcode()}")
            print(f"レスポンス: {res_body}")
            
            res_json = json.loads(res_body)
            if res_json.get("status") == "success":
                key = res_json.get("key")
                print(f"✅ 発行成功！ 新しいキー: {key}")
                
                # 2. GET (検証) のテスト
                print(f"\n[2/2] ライセンス検証テスト (GET) を開始します: {key}")
                verify_url = f"{GAS_URL}?license_key={key}"
                req_get = urllib.request.Request(verify_url, method='GET')
                with urllib.request.urlopen(req_get, context=ctx, timeout=10) as response_get:
                    res_get = response_get.read().decode('utf-8')
                    print(f"ステータスコード: {response_get.getcode()}")
                    print(f"レスポンス: {res_get}")
                    if '"valid":true' in res_get:
                        print("✅ 検証成功！ 正常に動作しています。")
                    else:
                        print("❌ 検証失敗。SSへの書き込みが遅れているか、シートが見つかっていません。")
            else:
                print(f"❌ 発行失敗: {res_json.get('message')}")
                
    except Exception as e:
        print(f"❌ 通信エラー: {e}")
        print("\n[確認事項]")
        print("1. GASの[デプロイ] > [新しいデプロイ] または [デプロイを管理] で正しく公開されていますか？")
        print("2. アクセスできるユーザーが「全員 (Anyone)」になっていますか？")
        print("3. インターネット接続は正常ですか？")

if __name__ == "__main__":
    diagnose()
