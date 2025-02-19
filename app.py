import os
import requests
import time
import hashlib
import hmac
from flask import Flask, jsonify

app = Flask(__name__)

# Shopee APIのテスト環境用の情報
PARTNER_ID = 1264951  # Test Partner ID
PARTNER_KEY = "656b4173764a646b757057416954506d635a7259736e4e63507172756f556143"  # Test API Partner Key
SHOP_ID = 123456789  # あなたのShopeeショップID（後で取得する）

# Shopee APIのエンドポイント（テスト環境）
API_HOST = "https://partner.test-stable.shopeemobile.com"

def generate_signature(path, timestamp):
    base_string = f"{PARTNER_ID}{path}{timestamp}"
    signature = hmac.new(PARTNER_KEY.encode(), base_string.encode(), hashlib.sha256).hexdigest()
    return signature

@app.route("/get_shop_info")
def get_shop_info():
    path = "/api/v2/shop/get_shop_info"
    timestamp = int(time.time())

    url = f"{API_HOST}{path}?partner_id={PARTNER_ID}&timestamp={timestamp}&sign={generate_signature(path, timestamp)}"
    headers = {"Content-Type": "application/json"}
    
    response = requests.get(url, headers=headers)

    return jsonify(response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
