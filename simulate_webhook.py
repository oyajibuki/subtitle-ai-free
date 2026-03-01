import urllib.request
import json
import ssl

url = "https://script.google.com/macros/s/AKfycbw-GQUSSCTIbSRLMhaItLX6GZSi0iemw5Vaxo0oKB4Rg9OOf1xJ4UEBJHczY7-3LWPj_Q/exec"

# Stripe決済のダミーJSONペイロードを作成
dummy_payload = {
    "type": "checkout.session.completed",
    "data": {
        "object": {
            "id": "cs_test_dummy_session_12345",
            "customer_details": {
                "email": "test-ai-subtitle@example.com"
            }
        }
    }
}

data = json.dumps(dummy_payload).encode('utf-8')
headers = {'Content-Type': 'application/json'}
req = urllib.request.Request(url, data=data, headers=headers, method='POST')

try:
    print("Sending POST request to GAS...")
    # bypass SSL if needed (but usually Google is fine)
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx) as response:
        result = response.read().decode('utf-8')
        print(f"Status Code: {response.getcode()}")
        print(f"Response: {result}")
except Exception as e:
    print(f"Error occurred: {e}")
