import urllib.request
import json
import ssl
import sys
import random
import string

# あなたのGASデプロイURL
GAS_URL = "https://script.google.com/macros/s/AKfycbw-GQUSSCTIbSRLMhaItLX6GZSi0iemw5Vaxo0oKB4Rg9OOf1xJ4UEBJHczY7-3LWPj_Q/exec"

def generate_free_license(email="test@example.com"):
    # 重複チェックを回避するためにランダムなセッションIDを生成
    session_id = "test_free_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    
    payload = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": session_id,
                "customer_details": {
                    "email": email
                }
            }
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(GAS_URL, data=data, headers=headers, method='POST')
    
    try:
        print(f"[{email}] へのライセンス発行リクエストを送信中...")
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get("status") == "success":
                print("✅ 成功しました！Googleスプレッドシートとメールを確認してください。")
            else:
                print(f"❌ 失敗: {result.get('message', '不明なエラー')}")
            print(f"応答内容: {result}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    target_email = sys.argv[1] if len(sys.argv) > 1 else "oyajibuki@gmail.com"
    generate_free_license(target_email)
